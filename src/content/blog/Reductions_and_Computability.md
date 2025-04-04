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

It can be noted that mapping reduction is, in fact, an independent process—not directly tied to decidability or recognizability—but it can be used to prove both. This proof technique also plays an important role in many other areas, such as complexity theory.



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




