---
title: 'Reductions and Computability'
description: ""
pubDate: 'Apr 03 2025'
tags: ['Computability Theory']
---

## Introduction

In computability theory, it can be somewhat tedious to analyze the decidability and recognizability of each decision problem from scratch—especially when the problems are closely related. For example, we already know that the Halting Problem

$$
\text{HALT} = \{ \langle y, x \rangle \in \Sigma^* \times \Sigma^* \mid y = \text{code}(M) \text{ and } M \text{ halts on } x \}
$$

is undecidable. Now suppose the problem is slightly changed: does a given Turing machine halt on *all* inputs? Or does it halt on the *empty* input? Are these problems decidable?

In such cases, a general strategy for proving undecidability is:

1. Assume there exists a Turing machine $M$ that decides the target problem.
2. Use $M$ to construct a machine $M_H$ that decides $\text{HALT}$.
3. Contradiction—since $\text{HALT}$ is known to be undecidable.

Abstracting this idea, to prove that a problem $A$ is undecidable, we assume that $A$ is decidable and show that this would imply the decidability of another problem $B$ that is already known to be undecidable. Therefore, $A$ cannot be decidable. **Mapping reduction** provides a unified and formal method for solving such problems.



## Definition of Mapping Reduction

The idea of a mapping reduction is to transform one problem into another. It is formally defined as follows:

Let $L_1$ and $L_2$ be languages over alphabets $\Sigma$ and $\Gamma$, respectively. A **mapping reduction** from $L_1$ to $L_2$ is a computable total function $f: \Sigma^* \to \Gamma^*$, such that
$$
x \in L_1 \iff f(x) \in L_2.
$$  
If such a function $f$ exists, we write $L_1 \leq_m L_2$.

A computable total function means that there exists a Turing machine which computes $f$, and it halts on every input $x \in \Sigma^*$. In other words, the function always produces an output rather than looping indefinitely.

The condition $x \in L_1 \iff f(x) \in L_2$ is equivalent to:  
- if $x \in L_1$, then $f(x) \in L_2$, and  
- if $x \notin L_1$, then $f(x) \notin L_2$.  

In other words, **YES-instances** of the decision problem for $L_1$ are mapped to YES-instances of the problem for $L_2$, and **NO-instances** of $L_1$ are mapped to NO-instances of $L_2$.

In fact, a mapping reduction is a concrete realization of the step 2 in the general proof strategy for undecidability we mentioned earlier—it directly transforms one problem into another. The hypothetical machine $M$ is only used at the final step to reach a contradiction.

It can be noted that mapping reduction is, in fact, an **independent process**—not directly tied to decidability or recognizability—but it can be used to prove both. This proof technique also plays an important role in many other areas, such as complexity theory.



## Example

Now, when we attempt to prove that a language $L$ is undecidable, it suffices to show that there exists a function $f$ such that  
$$
\text{HALT} \leq_m L,
$$  
i.e., $f$ reduces $\text{HALT}$ to $L$. If $L$ were decidable by some Turing machine $M$, then $\text{HALT}$ could also be decided by composing $M$ with $f$ (as shown below), leading to a contradiction. Therefore, $L$ must be undecidable.

<div style="overflow-x: auto; white-space: nowrap;">
  <table style="border-spacing: 0;">
    <tr>
      <td><img src="/images/blog/reduction_and_computability/htm.svg" alt="HTM" width="800"/></td>
    </tr>
  </table>
</div>



## Mapping Reduction in Computability Theory

If $L_1 \leq_m L_2$, then there exists a Turing machine that transforms the decision problem of $L_1$ into the decision problem of $L_2$. This means that, in terms of computability, if we can solve $L_2$, then we can solve $L_1$. In other words, if we know the hardness of $L_1$, then $L_2$ is at least as hard as $L_1$. Conversely, if we know the hardness of $L_2$, then $L_1$ is at most as hard as $L_2$.

Formally, for any languages $L_1$ and $L_2$, mapping reduction has the following properties:

- If $L_2$ is decidable and $L_1 \leq_m L_2$, then $L_1$ is decidable. (The following Turing machine decides $L_1$.)

<div style="overflow-x: auto; white-space: nowrap;">
  <table style="border-spacing: 0;">
    <tr>
      <td><img src="/images/blog/reduction_and_computability/htm2.svg" alt="HTM" width="600"/></td>
    </tr>
  </table>
</div>

- If $L_1$ is undecidable and $L_1 \leq_m L_2$, then $L_2$ is undecidable. (Logically equivalent to the above)

- If $L_2$ is decidable and $L_1$ is undecidable, then $L_1 \not\leq_m L_2$. (Also logically equivalent)

For recognizability:

- If $L_2$ is recognizable and $L_1 \leq_m L_2$, then $L_1$ is recognizable. (The following Turing machine recognize $L_1$.)

<div style="overflow-x: auto; white-space: nowrap;">
  <table style="border-spacing: 0;">
    <tr>
      <td><img src="/images/blog/reduction_and_computability/htm3.svg" alt="HTM" width="600"/></td>
    </tr>
  </table>
</div>

- If $L_1$ is not recognizable and $L_1 \leq_m L_2$, then $L_2$ is not recognizable.
- If $L_2$ is recognizable and $L_1$ is not recognizable, then $L_1 \not\leq_m L_2$.



## The Empty String Halting Problem

The **Empty String Halting** (ETH) problem asks whether a given Turing machine halts on the empty string. This problem may sound much simpler than the general Halting Problem, since the input is restricted to just one specific case. It is formally defined as:

$$
\text{ETH} = \{ x \in \Sigma^* \mid x = \text{code}(M) \text{ and } M \text{ halts on } \varepsilon \}.
$$

However, we will prove that $\text{HALT} \leq_m \text{ETH}$, thereby showing that $\text{ETH}$ is undecidable.

To prove that $\text{HALT} \leq_m \text{ETH}$, we need to construct a computable function $f$ such that:

$$
\begin{aligned}
\langle y, x \rangle \in \text{HALT} &\implies f(\langle y, x \rangle) \in \text{ETH} \\
\langle y, x \rangle \notin \text{HALT} &\implies f(\langle y, x \rangle) \notin \text{ETH}
\end{aligned}
$$

Consider the following construction:

- Check whether $\langle y, x \rangle$ is a valid encoding—that is, whether $y$ is the encoding of some Turing machine.  
  If not, let $f(\langle y, x \rangle) = y$. Clearly, $y \notin \text{ETH}$.

- Otherwise, let $M = \text{decode}(y)$, and define $f(\langle y, x \rangle) = \text{code}(M_{M,x})$, where $M_{M,x}$ is constructed as follows:
  - On any **non-empty** input, $M_{M,x}$ enters an infinite loop.
  - On the **empty** input, $M_{M,x}$ simulates $M$ on input $x$.

Now, for a valid encoding $\langle y, x \rangle$:

- If $\langle y, x \rangle \in \text{HALT}$, then $M_{M,x}$ halts on the empty input, so $f(\langle y, x \rangle) = \text{code}(M_{M,x}) \in \text{ETH}$.
- If $\langle y, x \rangle \notin \text{HALT}$, then $M_{M,x}$ does not halt on the empty input, so $f(\langle y, x \rangle) = \text{code}(M_{M,x}) \notin \text{ETH}$.

For an invalid encoding $\langle y, x \rangle$, we have $\langle y, x \rangle \notin \text{HALT}$, and $f(\langle y, x \rangle) = y \notin \text{ETH}$.

The rule "*on any non-empty input, $M_{M,x}$ enters an infinite loop*" is only used to define the behavior on non-empty inputs and ensure the computability of $f$.



## Limits of Mapping Reduction from Easy Problems

In the example above, we reduced a provenly hard decision problem ($\text{HALT}$) to a seemingly simpler one ($\text{ETH}$) via a mapping reduction, in order to demonstrate that the latter is equally hard. We also know that we can reduce a seemingly hard problem to a known easy one in order to solve it directly. But what happens if we reduce a provenly easy problem to another problem?

The answer is that we only learn that the latter is at least as “hard” as the former—which is not very helpful. In fact, for sufficiently simple decision problems, such as decidable languages, it is possible to reduce them to any nontrivial language $L$, that is, any $L \neq \Sigma^*$ and $L \neq \emptyset$.

For any decidable language $L_1$ and any nontrivial language $L_2$, suppose $M$ decides $L_1$. Since $L_2$ is nontrivial, we can find strings $y \in L_2$ and $z \notin L_2$. Now consider the function $f$ defined as follows:

$$
f(x) =
\begin{cases}
y & \text{if } M \text{ accepts } x \\
z & \text{if } M \text{ rejects } x
\end{cases}
$$

If $x \in L_1$, then $M$ accepts $x$, so $f(x) = y \in L_2$.  
If $x \notin L_1$, then $M$ rejects $x$, so $f(x) = z \notin L_2$.

This kind of construction relies on the assumption that $L_1$ is simple enough—that is, there exists a Turing machine $M$ that decides it.



## Rice’s Theorem

Finally, we use mapping reduction to prove **Rice’s Theorem**.

> Any nontrivial property about the language $L(M)$ recognized by a Turing machine $M$ is undecidable.  
> — Rice’s Theorem

Nontrivial means that not all recognizable languages $L(M)$ have the property, and not none of them do either.

First, we need to understand what a *property about a language $L(M)$* means. Formally, for any nontrivial set of Turing-recognizable languages $\mathcal{S} \subset \{ L(M) \mid M \text{ is a Turing machine} \}$, with $\mathcal{S} \neq \emptyset$, we define the language property:

$$
P = \{ \text{code}(M) \mid L(M) \in \mathcal{S} \}
$$

Note that $P$ is a set of Turing machine codes, **not** a set of languages. This refers to a property of the Turing machine $M$, but one that depends **only** on the language it recognizes. A language $L(M)$ is a subset of $\Sigma^*$, and any description of this set constitutes a language property. For example: whether $L(M)$ is finite, or whether the string "abc" belongs to $L(M)$, are both properties of the language $L(M)$.

In other words, even if two Turing machines $M_1$ and $M_2$ are different, as long as they recognize the same language—that is, $L(M_1) = L(M_2)$—then we have $P(M_1) = P(M_2)$.

In contrast, properties that are related to the *implementation* of the Turing machine $M$ are *not* considered language properties. For instance: whether $M$ halts within 100 steps, or whether the size of its state set is less than 10.

As a result, Rice’s Theorem cannot be used to prove the undecidability of the Halting Problem, since that is a property of the machine, not of the language it recognizes.



### Proof

Fix a property $P$. Assume that the empty language does **not** have this property, i.e., $P(\text{code}(M_\emptyset)) = 0$. Since $P$ is nontrivial, there exists some language $L(M_P)$ such that $P(\text{code}(M_P)) = 1$. Now we construct a function $f$ as follows:

- If $\langle y, x \rangle$ is not a valid encoding (i.e., $y$ is not the encoding of any Turing machine), then let $f(\langle y, x \rangle) = \text{code}(M_\emptyset)$.
- Otherwise, let $M = \text{decode}(y)$, and define $f(\langle y, x \rangle) = \text{code}(M_{M,x})$, where $M_{M,x}$ is constructed as follows:
  1. On any input $z$, $M_{M,x}$ first simulates $M$ on input $x$;
  2. If $M$ halts, then it simulates $M_P$ on input $z$;
  3. If $M_P$ accept the input $z$, then $M_{M,x}$ accepts the input $z$.

Now, for a valid encoding $\langle y, x \rangle$:

- If $\langle y, x \rangle \in \text{HALT}$, then $M$ halts on input $x$. Then, if $M_P$ accepts some input $z$, so does $M_{M,x}$. In this case, $M_{M,x}$ recognizes the same language as $M_P$, so $P(\text{code}(M_{M,x})) = P(\text{code}(M_P)) = 1$.

- If $\langle y, x \rangle \notin \text{HALT}$, then $M$ does not halt on input $x$, so $M_{M,x}$ does not accept any input $z$. In this case, $M_{M,x}$ recognizes the same language as $M_\emptyset$, so $P(\text{code}(M_{M,x})) = P(\text{code}(M_\emptyset)) = 0$.

For an invalid encoding $\langle y, x \rangle$, we also have $\langle y, x \rangle \notin \text{HALT}$, and we defined $f(\langle y, x \rangle) = \text{code}(M_\emptyset)$, so $P(\text{code}(M_\emptyset)) = 0$.

<div style="overflow-x: auto; white-space: nowrap;">
  <table style="border-spacing: 0;">
    <tr>
      <td><img src="/images/blog/reduction_and_computability/htm4.svg" alt="HTM" width="700"/></td>
    </tr>
  </table>
</div>

In our construction, one of the key step is that when $\langle y, x \rangle \notin \text{HALT}$, the machine $M_{M,x}$ loops on every input, and  

$$
P(\text{code}(M_{M,x})) = P(\text{code}(M_\emptyset)) = 0.
$$

However, the assumption $P(\text{code}(M_\emptyset)) = 0$ is something we made. What if instead $P(\text{code}(M_\emptyset)) = 1$?

In that case, we can simply consider the **complement** property $\neg P$. Then we have shown that  

$$
\{ \text{code}(M) \mid \neg P(\text{code}(M)) = 1 \}
$$

is undecidable, which is logically equivalent to saying that  

$$
\{ \text{code}(M) \mid P(\text{code}(M)) = 1 \}
$$

is undecidable.



## Conclusion

At this point, we have developed an understanding of **mapping reduction** as a tool for transforming one decision problem into another. Mapping reductions are not only used in computability theory, but also play an important role in complexity theory, where they are applied in a similar way.

We then used mapping reductions to prove the undecidability of the **Empty String Halting** ($\text{ETH}$) problem and **Rice’s Theorem**, demonstrating that mapping reduction is a general and powerful technique.


---

**Acknowledgments**  
This blog references material from the slides of **COMP0017 Computability and Complexity Theory** at University College London.
