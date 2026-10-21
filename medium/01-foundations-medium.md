<!--
MEDIUM DRAFT: Applied Cryptography Explained, Part 1
How to publish:
  1. Paste the text into a new Medium story (headings, bold and code blocks carry over).
  2. At each [IMAGE: ...] line, upload the named PNG from images/01/ and use the caption given.
  3. Suggested tags: Cryptography, Cybersecurity, Information Security, Computer Science, Mathematics
-->

# What Does "128 Bits of Security" Actually Mean?

## Applied Cryptography Explained, Part 1: the distinguisher game behind almost every security definition

Every cryptography library advertises its security in bits. AES-128 gives "128 bits of security". A protocol is "secure up to the birthday bound". But what is actually being promised, and against whom?

This is the first article in a monthly series based on my notes from the Applied Cryptography course in my MSc Cybersecurity at Radboud University. Before looking at any specific algorithm, we need a language for talking about security, and that is what this part is about.

*The full series, with proper math rendering, lives on GitHub: [github.com/jainanushkarathod/applied-crypto](https://github.com/jainanushkarathod/applied-crypto).*

---

## What symmetric cryptography is for

Symmetric cryptography assumes two parties already share a secret key K. With it, they want two things:

- **Confidentiality:** an eavesdropper learns nothing useful about the messages.
- **Authenticity:** the receiver can detect if a message was forged or modified.

The core tools that deliver these:

- **Encryption** for confidentiality (AES-CTR, ChaCha20)
- **Message authentication codes (MACs)** for authenticity (HMAC, Poly1305)
- **Authenticated encryption** for both at once (AES-GCM, ChaCha20-Poly1305, Ascon)
- **Hashing**, unkeyed, but a building block inside almost everything above (SHA-2, SHA-3)

---

## Measuring security in bits

A scheme offers **s bits of security** if the best attack using 2ᵃ operations succeeds with probability roughly

```
Pr[success] ≈ 2ᵃ / 2ˢ
```

With s = 128, an attacker doing 2⁶⁴ operations succeeds with probability about 2⁻⁶⁴, which is negligible. To have a real chance, they need close to 2¹²⁸ operations.

Three things determine the security level, and the weakest one wins:

1. **Key length.** A k-bit key can always be found by trying all 2ᵏ keys, so security is at most k bits.
2. **The primitive.** The fixed-size building block (for example AES) must have no shortcut attacks.
3. **The mode.** The construction that processes arbitrary-length data must not add weaknesses of its own.

---

## Primitives and modes

It helps to split a scheme into two layers.

A **primitive** is a fixed-size function. AES maps a 128-bit block to a 128-bit block under a key.

A **mode** uses the primitive to process data of any length. Counter mode, written CTR[AES_K], turns AES into a stream cipher.

[IMAGE: layers.png | Caption: A primitive is trusted through cryptanalysis, a mode through a proof.]

The two layers earn our trust in very different ways. Nobody can *prove* AES is secure; we trust it because decades of public cryptanalysis have failed to break it. Modes, on the other hand, come with **security proofs**, always *relative to* the primitive. Those proofs come in two styles:

- **Reductionist proof:** "if you can break the mode, you can break the primitive."
- **Ideal-model proof:** "if the primitive were perfect, the mode would be secure."

> **Kerckhoffs's principle:** security must rely only on the secrecy of the key, never on keeping the algorithm secret. Everything in this series assumes the attacker knows exactly how the scheme works.

---

## The distinguisher game

Here is the idea that the rest of this series is built on.

An adversary, called a **distinguisher D**, is placed in front of one of two worlds, without being told which:

- the **real world**: the actual scheme, with a secret random key;
- the **ideal world**: a perfectly random object with the same interface.

D sends queries, looks at the answers, and finally guesses which world it was in.

[IMAGE: distinguisher.png | Caption: The distinguisher must tell the real scheme apart from a perfectly random object.]

Its **advantage** measures how much better than a coin flip it does:

```
Adv(D) = | Pr[D outputs 1 in real world] − Pr[D outputs 1 in ideal world] |
```

An advantage of 0 means D cannot tell the worlds apart at all. An advantage close to 1 means the scheme is broken.

Why is this the right definition? If no realistic adversary can tell the scheme from something perfectly random, then any attack on the scheme would also have to work against perfect randomness, which is impossible.

**Resources matter.** We measure the adversary by two numbers:

- **q, data complexity:** the number of queries to the keyed system. These are online and usually limited, because each one needs the real key holder.
- **t, time complexity:** everything the adversary does offline, such as trying candidate keys.

We then write Adv(q, t) for the best advantage any adversary can reach with those resources.

---

## PRF security: what a good stream cipher looks like

A **stream cipher** takes a key K and a **diversifier** (a nonce) D, and produces a keystream Z. Encryption is just

```
C = M ⊕ Z
```

The diversifier **must be unique** per message. Reuse it and you get the same keystream twice, so C ⊕ C′ = M ⊕ M′: the XOR of two plaintexts leaks.

*Real-world example:* pay-TV and mobile telephony send data in short, numbered frames. The frame number is a ready-made diversifier.

A good stream cipher should look like fresh random bits for every new diversifier. So we compare it to a **random oracle**, a function returning independent random bits for each new input. That comparison is called **PRF security** (pseudorandom function).

---

## PRP and SPRP security: what a good block cipher looks like

A **block cipher** E_K maps an n-bit block to an n-bit block, and for each key it is a **permutation**: it can be inverted.

So the right ideal object is a **random permutation**, not a random function:

- **PRP security:** the adversary can only encrypt, and must tell E_K from a random permutation.
- **SPRP security (strong PRP):** the adversary can also *decrypt*, and must tell (E_K, E_K⁻¹) from a random permutation and its inverse.

SPRP matters whenever an attacker can get chosen ciphertexts decrypted, which happens in many real protocols.

### Connecting the layers: CTR mode

CTR mode uses a block cipher to build a keystream: Z = E_K(N‖1) ‖ E_K(N‖2) ‖ … Its security proof says:

```
Adv_prf[CTR](q, t) ≤ Adv_prp[E](q, t) + q² / 2ⁿ⁺¹
```

Read it term by term:

- **First term:** if AES is a good PRP, this is tiny.
- **Second term:** the price of using a permutation where a random function is wanted. A random permutation *never* repeats an output, while a random function starts repeating after about 2^(n/2) outputs (the birthday bound). An attacker watching many blocks can notice the suspicious absence of repeats. For AES, with n = 128, keep well below 2⁶⁴ blocks per key and this term stays negligible.

That is where the phrase "secure up to the birthday bound" comes from.

---

## Key recovery is also a distinguisher

The most obvious attack, trying every key, fits neatly into the same game.

[IMAGE: keysearch.png | Caption: Exhaustive key search, written as a distinguisher.]

1. Make one query and get C = O(0).
2. Offline, try t candidate keys K′ and check whether E_K′(0) = C.
3. If any key matches, guess "real world".

In the real world this succeeds when the true key is among the t guesses, probability about t / 2ᵏ. In the ideal world a match is pure accident. So for **every** block cipher:

```
Adv_sprp(q, t) ≳ t / 2ᵏ
```

No matter how well it is designed, a cipher with a k-bit key offers **at most k bits of security**. That is the formal version of "key length caps security".

---

## Key takeaways

- "s bits of security" means an attack costing 2ᵃ succeeds with probability about 2ᵃ / 2ˢ.
- Primitives are trusted through cryptanalysis; modes are trusted through proofs relative to the primitive.
- Most security definitions are **distinguisher games**: real scheme versus a perfectly random object.
- **PRF** compares to a random function, **PRP** to a random permutation, **SPRP** also allows decryption queries.
- Using a permutation as a function costs a **birthday-bound** term of about q² / 2ⁿ.
- Exhaustive key search means a k-bit key gives **at most k bits** of security.

**Next month, Part 2:** stream ciphers, block ciphers and AES: what happens inside an AES round, and why ECB mode leaks the shape of your data.

*These are personal study notes rather than official course material. Spotted a mistake? Let me know in the comments or open an issue on GitHub.*
