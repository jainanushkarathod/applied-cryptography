# Module 12: Commitments, Zero Knowledge and Discrete-Log Signatures

*How can you prove you know a secret without revealing anything about it, and how does that idea turn into Schnorr signatures, DSA and ECDSA?*

Module 11 built signatures from a trapdoor permutation (RSA). This module takes a completely different route, based on the discrete logarithm problem and on **interactive proofs**. We start with **commitment schemes**, move to **zero-knowledge proofs** and the **Schnorr identification protocol**, and then use the **Fiat-Shamir transform** to turn that protocol into a signature scheme. The same structure underlies DSA and ECDSA, which are also famously fragile, as Sony found out.

---

## 1. Commitment schemes

### Motivation: flipping a coin over the phone

Alice and Bob want to settle a bet with a coin flip, but they are not in the same room. If Alice flips and announces the result, she can lie. If Bob calls "heads" first and Alice flips after, she can still lie. Each party can cheat.

What they need is a **locked box**:

1. Alice flips the coin, puts the result in a box, locks it, and sends the box to Bob. This is the **commitment**.
2. Bob, who cannot see inside the box, announces his guess.
3. Alice sends the key; Bob opens the box. This is the **opening**. Whoever's prediction matches wins.

The box must have two properties:

- **Hiding:** Bob cannot see what is inside before opening it.
- **Binding:** Alice cannot change what is inside after sending it.

### Definition

A commitment scheme consists of three algorithms:

- $\mathrm{Setup}(1^\lambda) \to pk$: generates public parameters.
- $\mathrm{Comm}(pk, M; r) \to (C, D)$: using randomness $r$, produces a **commitment** $C$ and an **opening** (decommitment) $D$.
- $\mathrm{Open}(pk, C, D) \to M$ or $\bot$: recovers the committed message, or rejects an invalid opening.

**Correctness:** $\mathrm{Open}(pk, \mathrm{Comm}(pk, M; r)) = M$ for all $M$.

Often the opening is simply $D = (M, r)$, and verification consists of re-running $\mathrm{Comm}$ and checking that the result matches $C$.

### Binding and hiding, in three strengths

**Binding:** the committer cannot open $C$ to two different messages.

- **Perfect (unconditional):** for each $C$, there exists only one message it can be opened to. Even an attacker with unlimited computing power cannot cheat.
- **Statistical:** the probability that a commitment can be opened in two ways is negligible, even for an unbounded attacker.
- **Computational:** an efficient attacker finds two valid openings with only negligible probability.

**Hiding:** $C$ reveals nothing about $M$.

- **Perfect:** commitments to any two messages have **identical** distributions.
- **Statistical:** the distributions are statistically close (negligible distance).
- **Computational:** no efficient algorithm can tell them apart.

**You cannot have both perfect binding and perfect hiding.** If the scheme is perfectly binding, each commitment corresponds to exactly one message, so an unbounded attacker can try every message and randomness until it finds the one that produces $C$; hiding fails. If it is perfectly hiding, every commitment can be produced by many messages, so an unbounded committer can find a second opening; binding fails. At most one of the two can be unconditional.

### Hash-based commitments

The simplest practical commitment uses a hash function:

$$
C = H(M \Vert r), \qquad D = (M, r).
$$

- **Computationally binding** if $H$ is collision-resistant: two openings $(M, r) \neq (M', r')$ with the same $C$ would be a collision.
- **Hiding** relies on the randomness $r$: without it, an attacker could just hash every plausible $M$ and compare. In the random oracle model, with enough random bits in $r$, the commitment is statistically hiding.

### Pedersen commitments

Let $G$ be a group of prime order $q$ with generators $g$ and $h$, chosen so that **nobody knows** $\log_g h$. To commit to $m \in \mathbb{Z}_q$ with randomness $r \in \mathbb{Z}_q$:

$$
C = g^{r} h^{m}.
$$

For the coin-flip example, $m$ is a single bit, so the commitment is either $g^r$ or $g^r h$.

- **Perfectly hiding.** For any fixed $m$, $g^r$ is a uniformly random group element, so $C = g^r h^m$ is uniformly random too. Commitments to $0$ and to $1$ have exactly the same distribution.
- **Computationally binding** under the discrete logarithm assumption. Suppose Alice could open $C$ in two ways, $g^{r_0} h^{m_0} = g^{r_1} h^{m_1}$ with $m_0 \neq m_1$. Then $g^{r_0 - r_1} = h^{m_1 - m_0}$, so

$$
\log_g h = \frac{r_0 - r_1}{m_1 - m_0} \bmod q,
$$

and she would have solved a discrete logarithm problem.

Pedersen commitments are also **homomorphic**: multiplying two commitments gives a commitment to the sum of the messages. This makes them very useful in voting, confidential transactions and zero-knowledge protocols.

---

## 2. Zero-knowledge proofs

A **zero-knowledge (ZK) protocol** lets a prover $P$ convince a verifier $V$ that it knows a secret (or that a statement is true) **without revealing the secret**. They exchange messages in an **interactive proof**.

Formally, there is a public statement $x$ (for example, a public key) and a language $L$ of true statements; the prover holds a secret **witness** (for example, the private key). The protocol should be:

- **Complete:** if $x \in L$ and the prover is honest, the verifier always (or almost always) accepts.
- **Sound:** if $x \notin L$, no cheating prover $P^*$ can make the verifier accept, except with small probability, called the **soundness error**.
- **Zero-knowledge:** the verifier learns nothing beyond the fact that the statement is true, **even if it cheats**.

### What "learns nothing" means

The **transcript** of a run is the sequence of messages exchanged. The zero-knowledge property says: for every verifier strategy $V^*$, there is an efficient **simulator** that, **without the secret**, produces transcripts that are indistinguishable from real conversations between $P$ and $V^*$.

If the verifier could have produced the whole conversation by itself, the conversation cannot have taught it anything it could not already compute. In particular, a verifier who has seen a real proof cannot later use it to convince someone else that *it* knows the secret: anyone can produce a convincing-looking transcript after the fact, so the transcript itself proves nothing to a third party.

---

## 3. The Schnorr identification protocol

Let $G$ be a cyclic group of prime order $q$ with generator $g$, in which the discrete logarithm problem is hard. The prover's secret key is $w \in \mathbb{Z}_q$; the public key is $v = g^w$. The prover wants to show it knows $w$.

| Step | Prover $P$ (knows $w$) | | Verifier $V$ (knows $v = g^w$) |
|---|---|---|---|
| 1. Commitment | choose random $u \in \mathbb{Z}_q$, compute $a = g^u$ | $\xrightarrow{\;a\;}$ | |
| 2. Challenge | | $\xleftarrow{\;ch\;}$ | choose random challenge $ch$ |
| 3. Response | $resp = u + ch \cdot w \bmod q$ | $\xrightarrow{\;resp\;}$ | accept iff $g^{resp} = a \cdot v^{ch}$ |

**Completeness.** For an honest prover,

$$
g^{resp} = g^{u + ch\cdot w} = g^u \cdot (g^w)^{ch} = a \cdot v^{ch}.
$$

**Why the fresh $u$ matters.** The response $resp = u + ch \cdot w$ contains the secret $w$, but it is masked by the random $u$, which acts like a one-time pad in $\mathbb{Z}_q$. As long as $u$ is fresh and uniformly random in every run, $resp$ is uniformly random and reveals nothing about $w$, whatever challenge the verifier sends. If $u$ were ever reused with two different challenges, the verifier could solve for $w$ (see special soundness below, and the PlayStation 3 story in Section 6).

**Soundness.** A cheating prover who does not know $w$ can still succeed if it **guesses the challenge in advance**:

1. Guess $ch^*$ and pick any $resp$.
2. Send $a = g^{resp} \cdot v^{-ch^*}$.
3. If the verifier indeed sends $ch^*$, respond with $resp$; the check $g^{resp} = a \cdot v^{ch^*}$ passes.

So the soundness error equals the probability of guessing the challenge, $1/|\mathcal{C}|$ for a challenge set $\mathcal{C}$.

- With a **one-bit** challenge, $ch \in \{0, 1\}$, the soundness error is $1/2$ per run. To reach $2^{-128}$, the protocol must be repeated 128 times, which is expensive.
- Schnorr's improvement: choose $ch$ from a **large** set (for example, all of $\mathbb{Z}_q$, or $t$-bit strings). Then one run already has soundness error $1/|\mathcal{C}|$, which is negligible.

The price of the large challenge is that we only know how to prove zero-knowledge against an **honest verifier**, one that picks its challenge uniformly at random. That turns out to be exactly what is needed for signatures.

---

## 4. Sigma protocols

The Schnorr protocol is the prototype of a **Σ-protocol**: a three-move protocol (commitment $a$, challenge $ch$, response $resp$) with three properties.

**Completeness.** As before.

**Special soundness.** Given two accepting transcripts with the **same commitment** and **different challenges**, $(a, ch, resp)$ and $(a, ch', resp')$ with $ch \neq ch'$, one can efficiently **extract** the secret. For Schnorr:

$$
g^{resp} = a v^{ch},\quad g^{resp'} = a v^{ch'} \;\Longrightarrow\; g^{resp - resp'} = v^{ch - ch'} \;\Longrightarrow\; w = \frac{resp - resp'}{ch - ch'} \bmod q.
$$

In other words, a prover who can answer two different challenges for the same commitment must know $w$. This is why special soundness is also called the existence of a **knowledge extractor**, and why it implies a soundness error of $1/|\mathcal{C}|$.

**Special honest-verifier zero knowledge (SHVZK).** There is a simulator that, given **any challenge** $ch$ in advance, outputs a transcript $(a, ch, resp)$ with the same distribution as a real one. For Schnorr, it is the cheating-prover trick from above: pick $resp$ uniformly at random and set $a = g^{resp} v^{-ch}$. The resulting $(a, resp)$ pair is distributed exactly like an honest one.

Σ-protocols are much easier to construct than fully zero-knowledge protocols, and they are exactly what the Fiat-Shamir transform needs.

---

## 5. Fiat-Shamir: from identification to signatures

In a Σ-protocol, the honest verifier's only job is to send a **random** challenge. The **Fiat-Shamir transform** (1986) replaces the verifier with a **hash function**, modelled as a random oracle:

$$
ch = H(a, M).
$$

This makes the protocol **non-interactive**: the prover computes the challenge itself. Because the challenge depends on $a$, the prover can no longer choose $a$ after knowing $ch$, which was the cheating strategy. By including a message $M$ in the hash, the proof becomes bound to that message, and we get a **signature**: "someone who knows $w$ produced this proof, for this message".

- **Signing:** run the prover, computing $ch = H(a, M)$ instead of waiting for a verifier. The signature is $\sigma = (a, resp)$ (or the equivalent $(ch, resp)$).
- **Verifying:** recompute $ch = H(a, M)$ and run the verifier's check.

Signer and verifier never interact, yet both compute the same challenge, because it is a deterministic function of public values. Security (EUF-CMA in the random oracle model) follows from special soundness and SHVZK, using a technique called the **forking lemma**: rewind the forger and give it a different hash answer, to obtain two transcripts with the same $a$ and different challenges.

### Schnorr signatures

Applying Fiat-Shamir to the Schnorr protocol gives **Schnorr signatures**. With secret key $x$ and public key $y = g^x$:

- **Sign:** choose a random $k \in \mathbb{Z}_q$, compute $r = g^k$, $h = H(M, r)$ and $s = k + h \cdot x \bmod q$. Output $\sigma = (h, s)$.
- **Verify:** compute $r' = g^{s} \cdot y^{-h}$ and accept iff $H(M, r') = h$.

Schnorr signatures are simple, efficient, and have a clean security proof. For a long time they were hardly used because they were **patented** (until 2008), which is precisely why NIST designed DSA instead. Today they are back: **EdDSA/Ed25519** is a Schnorr-type scheme over an elliptic curve, and Bitcoin adopted Schnorr signatures in 2021 (BIP 340).

---

## 6. DSA and ECDSA

### The Digital Signature Algorithm

**KeyGen** (same group structure as Schnorr):

1. Choose primes $p$ and $q$ with $q \mid p - 1$, and $g \in \mathbb{Z}_p^*$ of order $q$.
2. Choose a random private key $x \in \mathbb{Z}_q$ and compute $y = g^x \bmod p$.
3. Public key $pk = y$; private key $sk = x$.

**Sign** message $M$:

1. Choose a random **ephemeral key** (nonce) $k \in \mathbb{Z}_q$ and compute $r = (g^k \bmod p) \bmod q$.
2. Compute $h = H(M)$ and $s = (h + x r)\, k^{-1} \bmod q$.
3. Output $\sigma = (r, s)$.

**Verify:**

1. Check $0 < r, s < q$, and compute $h = H(M)$.
2. Compute $u_1 = h\, s^{-1} \bmod q$ and $u_2 = r\, s^{-1} \bmod q$.
3. Accept iff $(g^{u_1} y^{u_2} \bmod p) \bmod q = r$.

Compare with Schnorr: there, $h = H(M, r)$ and $s = k + h x$. DSA hashes only the message and mixes things differently, which avoided the patent but also complicates the security analysis.

**ECDSA** is the same scheme over an elliptic curve group: $r$ is the $x$-coordinate of the point $kG$, reduced modulo the group order. It gives the same security with much smaller keys.

### The ephemeral key $k$ is critical

DSA and ECDSA are extremely sensitive to the ephemeral key $k$. It must be **secret**, **unpredictable**, and **never reused**.

Suppose the same $k$ (hence the same $r$) is used to sign two messages $M_1, M_2$:

$$
s_1 = (H(M_1) + x r)\,k^{-1}, \qquad s_2 = (H(M_2) + x r)\,k^{-1}.
$$

Subtracting cancels the secret key:

$$
s_1 - s_2 = \big(H(M_1) - H(M_2)\big)\,k^{-1} \quad\Longrightarrow\quad k = \frac{H(M_1) - H(M_2)}{s_1 - s_2} \bmod q.
$$

With $k$ known, the private key follows from either signature:

$$
x = \frac{s_1 k - H(M_1)}{r} \bmod q.
$$

**The PlayStation 3.** In December 2010, the group fail0verflow announced that they had recovered the ECDSA private key Sony used to sign PlayStation 3 software. Sony's implementation used the **same, fixed $k$** for every signature. Two signatures were enough to compute $k$ and then the master signing key, after which anyone could sign software that the console would accept as genuine.

Even slightly **biased** nonces (a few predictable bits, leaked through timing) are enough for lattice attacks to recover the key from many signatures. The modern fix is to derive $k$ **deterministically** from the private key and the message, as in RFC 6979 and in EdDSA, so that it never depends on the quality of a random number generator.

---

## 7. Key sizes

NIST's recommendations (SP 800-57 and SP 800-131A) at the time of the course:

| Algorithm | Key size | Classical security | Status |
|---|---|---|---|
| RSA / DSA 1024 | 1024 | 80 bits | disallowed (legacy verification only) |
| RSA / DSA 2048 | 2048 | 112 bits | acceptable |
| RSA / DSA 3072 | 3072 | 128 bits | recommended |
| RSA / DSA 7680 | 7680 | 192 bits | long term |
| RSA / DLP 15360 | 15360 | 256 bits | long term |
| ECDSA-160 | 160 | 80 bits | disallowed (legacy verification only) |
| ECDSA-224 | 224 | 112 bits | acceptable |
| ECDSA-256 | 256 | 128 bits | recommended |
| ECDSA-384 | 384 | 192 bits | long term |
| ECDSA-512 (P-521) | 512+ | 256 bits | long term |

Elliptic curves achieve the same classical security with keys that are an order of magnitude smaller. NIST has since proposed deprecating 112-bit security after 2030, and phasing out RSA and elliptic-curve signatures entirely in favour of post-quantum schemes by 2035. None of these schemes resist a large quantum computer (Module 13).

---

## Key takeaways

- A **commitment** must be **hiding** and **binding**; both can be perfect, statistical or computational, but not both perfect at once.
- **Hash commitments** $H(M \Vert r)$ are simple; **Pedersen** commitments $g^r h^m$ are perfectly hiding, computationally binding under DL, and homomorphic.
- A **zero-knowledge** proof is complete, sound and simulatable: the verifier could have produced the transcript itself.
- **Schnorr identification**: $a = g^u$, random $ch$, $resp = u + ch \cdot w$; the fresh $u$ hides $w$, and soundness error is $1/|\mathcal{C}|$.
- **Σ-protocols** have special soundness (two transcripts reveal the secret) and SHVZK.
- **Fiat-Shamir** replaces the challenge with $H(a, M)$ and yields signatures such as Schnorr and EdDSA.
- **DSA/ECDSA** leak the private key if the ephemeral $k$ is ever reused, as the PlayStation 3 showed; derive $k$ deterministically.

**Previous:** [Module 11: Digital Signatures](11-digital-signatures.md) · **Next:** [Module 13: Post-Quantum and Hash-Based Signatures](13-hash-based-signatures.md)
