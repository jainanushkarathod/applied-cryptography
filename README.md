# Applied Cryptography: Explained

A module-by-module walkthrough of applied cryptography, from the security definitions behind AES and MACs to authenticated encryption, hashing, public-key schemes, post-quantum signatures, key exchange protocols and key management.

These notes started as my running notes for the **Applied Cryptography** course in my MSc Cybersecurity at Radboud University. I have rewritten them into self-contained explanations, with original diagrams and worked examples, aimed at anyone who knows basic discrete maths and wants to understand *why* constructions are designed the way they are.

> **Disclaimer:** These are personal study notes, not official course material. Errors are mine. Corrections and suggestions are welcome via issues or pull requests.

---

## How to read this

Each module is self-contained, but the order below builds up gradually. Part A covers symmetric cryptography, Part B public-key cryptography, and Part C protocols and practice.

### Part A: Symmetric cryptography

| # | Module | Topics |
|---|--------|--------|
| 1 | [Foundations of Symmetric Security](modules/01-foundations.md) | bits of security, primitives vs modes, distinguishers, PRF / PRP / SPRP, key recovery |
| 2 | [Stream Ciphers, Block Ciphers and AES](modules/02-block-ciphers-aes.md) | AES round function, ECB / CBC / OFB / CTR |
| 3 | [Message Authentication](modules/03-message-authentication.md) | MACs, unforgeability, universal hashing, Wegman-Carter, Poly1305, CBC-MAC |
| 4 | [Authenticated Encryption](modules/04-authenticated-encryption.md) | generic composition, GCM, nonce reuse, GCM-SIV |
| 5 | [Tweakable Block Ciphers](modules/05-tweakable-block-ciphers.md) | LRW, XEX, OCB, XTS, masking techniques |
| 6 | [Hash Functions](modules/06-hash-functions.md) | Merkle-Damgård, length extension, indifferentiability, sponges, Keccak / SHA-3 |
| 7 | [Key Derivation and Password Hashing](modules/07-key-derivation.md) | HMAC, HKDF, PBKDF2, disk encryption |
| 8 | [Keyed Sponges and Duplexes](modules/08-keyed-sponges.md) | SpongeWrap, Ascon, suffix-keyed sponge |

### Part B: Public-key cryptography

| # | Module | Topics |
|---|--------|--------|
| 9 | [Public-Key Foundations](modules/09-public-key-foundations.md) | hardness assumptions, reductions, IND-CPA / IND-CCA, textbook RSA attacks |
| 10 | [KEMs and the Fujisaki-Okamoto Transforms](modules/10-kems-fo-transforms.md) | KEM security, FO transforms |
| 11 | [Digital Signatures](modules/11-digital-signatures.md) | EUF-CMA, RSA-FDH, RSA-PSS |
| 12 | [Commitments, Zero Knowledge and Discrete-Log Signatures](modules/12-commitments-zero-knowledge.md) | Pedersen, Schnorr, sigma protocols, Fiat-Shamir, DSA / ECDSA |
| 13 | [Post-Quantum and Hash-Based Signatures](modules/13-hash-based-signatures.md) | quantum threat, Lamport, Merkle trees, WOTS, XMSS / LMS, SPHINCS+ |

### Part C: Protocols and practice

| # | Module | Topics |
|---|--------|--------|
| 14 | [Authenticated Key Exchange](modules/14-authenticated-key-exchange.md) | Diffie-Hellman, STS, SIGMA, IKE, TLS 1.2 vs 1.3 |
| 15 | [Key Management](modules/15-key-management.md) | ISO 11568, key lifecycle, secret sharing, key hierarchy, HSMs, smart cards |

---

## Notation used throughout

| Symbol | Meaning |
|--------|---------|
| $K$ | secret key, $k$ bits long |
| $n$ | block size (or output size) in bits |
| $M, C, T$ | message, ciphertext, tag |
| $N$ | nonce |
| $\oplus$ | bitwise XOR |
| $\Vert$ | concatenation |
| $\mathcal{D}$ | distinguisher (an adversary trying to tell two worlds apart) |
| $q$ | data complexity: number of queries to the keyed system |
| $t$ | time complexity: offline computation by the adversary |
| $\mathsf{RO}$ | random oracle (ideal random function) |
| $p$ | random permutation |

---

## Repository layout

```
modules/     one Markdown file per module (math renders on GitHub)
images/      diagrams used in the modules, as SVG and PNG
diagrams/    Python source for every diagram (python3 diagrams/draw.py regenerates them)
medium/      Medium-ready versions of the modules (plain-text math, no tables)
```

All diagrams are original drawings made for this repository.

## Also on Medium

A version of each module is published monthly on [Medium](https://jainanushka.medium.com).

## License

<!-- TODO: choose a license, e.g. CC BY 4.0 for the text -->
