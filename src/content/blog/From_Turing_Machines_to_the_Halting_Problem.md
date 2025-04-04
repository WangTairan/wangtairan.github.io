---
title: 'From Turing Machines to the Halting Problem'
description: "An introduction to Turing machines, decision problems, and the proof of the Halting Problem's undecidability."
pubDate: 'Apr 01 2025'
tags: ['Computability Theory']
---

## Why Turing Machines?

If you know a bit about Turing machines, you might wonder: in an era where computing devices have gone through countless iterations, the Turing machine seems like an awkward and inefficient model. Any modern device appears far more elegant and fast. So, is it still necessary to understand the Turing machine? What can it possibly offer us today?

For the first question, the answer is: it depends. If you're not interested in computability or complexity theory and your focus is purely on applications, then you might not need to study Turing machines at all.

For the second question, the Turing machine offers a formal mathematical model for rigorous proofs — and it's surprisingly powerful:

- The Church–Turing thesis tells us that any computable problem can be solved by a Turing machine. This means anything your computer can do—or anything you can program in Python, Haskell, or C—can also be done by a Turing machine. In terms of computational power, they are equivalent.

- If an algorithm runs in polynomial time on a Turing machine, it will also run in polynomial time on a RAM model—that is, on real-world devices like smartphones and computers.

> Any function that can be computed algorithmically can also be computed by a Turing machine.  
> — Church–Turing Thesis

Therefore, if we prove that a problem cannot be solved by a Turing machine, then no programming language, RAM model, or even any other computing model can solve it.

If we prove an algorithm’s complexity is polynomial on the Turing machine model, it will belong to the same complexity class on any programming language or RAM-based device (though the actual runtime may differ). The same applies in reverse.

One of the most famous problems that a Turing machine cannot solve is the Halting Problem. By the end of this blog, we’ll see why.

## Definition of a Turing Machine

The idea of a Turing machine was first introduced by Alan Turing in 1936. A computable problem is written on an input tape, which extends infinitely to the right. The machine starts in an initial state with its read/write head pointing to the first symbol of the input. Based on a set of rules, the current symbol under the head, and its state, the Turing machine can:

- Update the symbol at the current position  
- Change its state  
- Move the head left or right  

When the computation finishes, the result remains on the tape.

<div style="overflow-x: auto; white-space: nowrap;">
    <table style="border-spacing: 0;">
        <tr>
            <td><img src="/images/blog/halting/tm1.svg" alt="TM1" width="300"/></td>
            <td><img src="/images/common/right_arr.svg" alt="Arrow" width="50"/></td>
            <td><img src="/images/blog/halting/tm2.svg" alt="TM2" width="300"/></td>
        </tr>
    </table>
</div>

Formally, a Turing machine is defined as a 5-tuple $\langle \Sigma, Q, q_0, H, \delta \rangle$:

- $\Sigma$ is a finite alphabet of symbols, including the blank symbol $\sqcup$.  
- $Q$ is a finite set of states.  
- $q_0 \in Q$ is the initial state.  
- $H \subseteq Q$ is the set of halting states.  
- $\delta$ is the transition function.

$\Sigma$ is used to represent the input on the tape—it can be as simple as $\{0, 1, \sqcup\}$, like a binary computer, or any alphabet that is easy to work with.  
$Q$ defines the machine’s states, $q_0$ tells it where to start, and $H$ defines the states where the machine should stop immediately.  
$\delta$ encodes the rules—the algorithm for solving the problem—and is usually written as:

$$
\delta : (Q \setminus H) \times \Sigma \rightarrow Q \times \Sigma \times \{\rightarrow, \leftarrow\}
$$

Here, $(Q \setminus H)$ is the current state, and $\Sigma$ is the current symbol under the head. Based on these, $\delta$ determines the next state, the new symbol to write, and the direction to move the head.

Note: Besides the 5-tuple definition, some conventions of Turing machines may vary—for example, whether the tape is infinite on both sides, or whether the head starts on the first input symbol or just before it. These conventions are ultimately reflected in the definitions of $Q$ and $\delta$.



## Example

Let’s define a Turing machine that inverts all the 0s and 1s in the input. For example, given `11001`, the output will be `00110`. Its 5-tuple is defined as:

$$
\Sigma = \{0, 1, \sqcup\}, \quad Q = \{q_0, q_H\}, \quad q_0 = q_0, \quad H = \{q_H\}
$$

The transition function is defined as:

$$
\begin{aligned}
\delta(q_0, 0) &= (q_0, 1, \rightarrow) \\
\delta(q_0, 1) &= (q_0, 0, \rightarrow) \\
\delta(q_0, \sqcup) &= (q_H, \sqcup, \rightarrow)
\end{aligned}
$$

For the input `10011`, the Turing machine runs on the tape as follows:
<div style="overflow-x: auto; white-space: nowrap;">
  <table style="border-spacing: 0;">
    <tr>
      <td><img src="/images/blog/halting/ex1.svg" alt="EX1" width="200"/></td>
      <td><img src="/images/common/right_arr.svg" alt="Arrow" width="50"/></td>
      <td><img src="/images/blog/halting/ex2.svg" alt="EX2" width="200"/></td>
      <td><img src="/images/common/right_arr.svg" alt="Arrow" width="50"/></td>
      <td><img src="/images/blog/halting/ex3.svg" alt="EX3" width="200"/></td>
      <td><img src="/images/common/right_arr.svg" alt="Arrow" width="50"/></td>
      <td><img src="/images/blog/halting/ex4.svg" alt="EX4" width="200"/></td>
      <td><img src="/images/common/right_arr.svg" alt="Arrow" width="50"/></td>
      <td><img src="/images/blog/halting/ex5.svg" alt="EX5" width="200"/></td>
      <td><img src="/images/common/right_arr.svg" alt="Arrow" width="50"/></td>
      <td><img src="/images/blog/halting/ex6.svg" alt="EX6" width="200"/></td>
      <td><img src="/images/common/right_arr.svg" alt="Arrow" width="50"/></td>
      <td><img src="/images/blog/halting/ex7.svg" alt="EX7" width="200"/></td>
    </tr>
  </table>
</div>

You may have noticed that for linear problems, a Turing machine can solve them quickly. But for nonlinear problems, the solutions are often less intuitive. Here, we only need to convince ourselves that any problem a computer can solve can also be solved by a specific Turing machine.



## Decision Problem

A decision problem is a type of problem with a YES or NO answer. For example, given a positive integer, determine whether it is even; or given a Turing machine and an input, determine whether the machine halts on that input. For such problems, the Turing machine does not need to write the answer on the tape. Instead, it uses two special halting states, $q_{accept}$ and $q_{reject}$, to represent acceptance and rejection. (This can easily be converted into writing the answer on the tape if needed.)

<div style="overflow-x: auto; white-space: nowrap;">
  <table style="border-spacing: 0;">
    <tr>
      <td><img src="/images/blog/halting/dtm.svg" alt="DTM" width="400"/></td>
    </tr>
  </table>
</div>

To formally define a decision problem, we consider that for any input string, there are two cases:
- The string is a YES instance.
- The string is a NO instance.

We define the set of all YES-instance strings as the language $L$ (languages are just subsets of $\Sigma^*$). A Turing machine that solves this decision problem acts as a decision function: when given input $x \in L$, it halts in state $q_{accept}$; otherwise, it halts in state $q_{reject}$.

For example, consider the problem of determining whether a number is even, and the Turing machine $ M$ that solves it.

The alphabet is $ \{0, 1, \dots, 9, \sqcup\}$, and the language $ L = \{\text{strings representing even numbers}\}$. Then, for input $ x = 12 \in L$, $ M(x)$ halts in state $ q_{accept}$. For input $ x = 7 \notin L$, $ M(x)$ halts in state $ q_{reject}$.



## Encoding

At this point, we have a basic understanding of how a Turing machine works. However, some parts are still lacking a formal definition—for example, the input $x$. For the same problem and data, the encoding is not unique.  

Take the parity-checking problem for positive integers as an example. If the alphabet is $\{0, 1, \dots, 9, \sqcup\}$, the input can be a string of decimal digits. Alternatively, we could represent the number in binary using only $\{0, 1, \sqcup\}$. Even with the alphabet fixed to $\{0, 1, \sqcup\}$, encoding is still not unique—for example, we could encode a number by repeating the symbol $1$: $2$ becomes `11`, and $5$ becomes `11111`.

Therefore, we need to define what makes an encoding valid or invalid. For a problem and data instance $\alpha$, a valid encoding system should satisfy:

1. If $\alpha \ne \beta$, then $\text{code}(\alpha) \ne \text{code}(\beta)$.
2. We should be able to determine whether a string $x \in \Sigma^*$ is a valid encoding of some $\alpha$.
3. It must be possible to recover the original $\alpha$ from $\text{code}(\alpha)$.

For point 2, recognizability helps us check whether the input is a valid instance of the problem. For example, in the positive integer parity-checking problem over the alphabet $\{0, 1, \dots, 9, \sqcup\}$, the string "0" is not a valid encoding, since 0 is not a positive integer. Therefore, it is not the encoding of any valid data $\alpha$. Other examples of invalid encodings might include $0034$ or $3\sqcup 5$.

In decision problems, inputs that are invalid or do not belong to the problem domain—along with the NO instances—together form the set of inputs that the Turing machine should reject.



## Decidability and Recognizability

Before we can decide whether a problem can be solved by a Turing machine, we must first define what it means for a problem to be **solved** by a Turing machine.  

For decision problems encoding as language $L$, we require that the Turing machine $M$ produces the correct answer in a finite number of steps. That is, if the data $\alpha$ is a YES-instance, the input $x=\text{code}(\alpha)\in L$, then $M(x)$ halts in $q_{accept}$ within a finite number of steps. If $\alpha$ is a NO-instance, the input $x=\text{code}(\alpha)\notin L$, or $x$ not a valid encoding, then $M(x)$ halts in $q_{reject}$ within a finite number of steps. At this point, we say that $M$ decides $L$.

If there exists a Turing machine $M$ that decides a language $L$, then the language and its corresponding decision problem are called **decidable**.

If no Turing machine $M$ exists that decides a language $L$, then the language and its corresponding decision problem are called **undecidable** or **unsolvable**.  

Among these, some problems are still **recognizable**—meaning there exists a Turing machine that accepts all YES-instances (and halts in finite steps), but dose not halt on NO-instances.

Clearly, the Halting Problem is a recognizable problem. We can simply run the given Turing machine on the given input (see following section): if the machine halts, we accept it. If it does not halt, we make no decision.



## Universal Turing Machine

So far, the Turing machines we've introduced are designed to solve specific tasks. This is quite different from modern computers, which allow us to run task-specific programs directly, rather than building a separate "machine" for each task. This leads to the concept of the **Universal Turing Machine (UTM)**.

A UTM takes as input a encoding of a Turing machine $M$ and an input $x$, then simulates the behavior of $M(x)$ and produces the same result.

A UTM does exist, and can be constructed in various ways. One possible structure is as follows:

- The input to the UTM is $\text{code}(M)\text{code}(x)$, where $\text{code}(M)$ includes all of $M$'s information and its transition function.
- The UTM checks whether $\text{code}(M)$ and $\text{code}(x)$ are valid. If not, it enters an infinite loop.
- The UTM then simulates $M(x)$: if $M(x)$ halts and produces an output $z$, the UTM does the same; if $M(x)$ loops forever, so does the UTM.



## The Undecidability of the Halting Problem

The Halting Problem is a decision problem: given a Turing machine $M$ and an input $x$, determine whether $M$ halts on $x$. The corresponding language can be defined as:

$$
\text{HALT} = \{ \langle y, x \rangle \in \Sigma^* \times \Sigma^* \mid y = \text{code}(M) \text{ and } M \text{ halts on } x \}
$$

We already know that $\text{HALT}$ is recognizable. Now, we will prove that it is undecidable.  

We use **proof by contradiction**: assume there exists a Turing machine $M_H$ that decides $\text{HALT}$.

Now we construct a Turing machine $M'$ that takes an input $z \in \Sigma^*$, then runs $M_H$ on input $\langle z, z \rangle$.  

- If $M_H$ accepts $\langle z, z \rangle$—meaning that running the decoded Turing machine $\text{decode}(z)$ on input $z$ halts—then $M'$ enters an infinite loop.  
- If $M_H$ rejects $\langle z, z \rangle$—meaning that $\text{decode}(z)$ on input $z$ does not halt or the encoding is invalid—then $M'$ accepts.

<div style="overflow-x: auto; white-space: nowrap;">
  <table style="border-spacing: 0;">
    <tr>
      <td><img src="/images/blog/halting/haltmd.svg" alt="DTM" width="600"/></td>
    </tr>
  </table>
</div>

Now consider feeding $\text{code}(M')$ as input to $M'$. The execution flow of $M'$ is as follows:

1. $M'$ runs $M_H$ on input $\langle \text{code}(M'), \text{code}(M') \rangle$.
2. Then $M_H$ decides whether $M'$ halts on input $\text{code}(M')$. If $M'$ halts on input $\text{code}(M')$, then $M_H$ accepts; otherwise, it rejects.
3. If $M_H$ accepts $\langle \text{code}(M'), \text{code}(M') \rangle$, then $M'$ enters an infinite loop;  
if $M_H$ rejects $\langle \text{code}(M'), \text{code}(M') \rangle$, then $M'$ accepts $\text{code}(M')$.

However:

- $M_H$ accepting $\langle \text{code}(M'), \text{code}(M') \rangle$ implies that $M'$ halts on input $\text{code}(M')$,  
but in fact $M'$ enters an infinite loop on that case.
- $M_H$ rejecting $\langle \text{code}(M'), \text{code}(M') \rangle$ implies that $M'$ does **not** halt on input $\text{code}(M')$,  
but in fact $M'$ halts.

This contradiction shows that no Turing machine $M_H$ can decide the language $\text{HALT}$.



## The Unrecognizability of the Complement of HALT

The language HALT is recognizable. As a direct consequence, its complement, $\text{HALT}^-$, is **not** recognizable.

$$
\text{HALT}^- = \{ \langle y, x \rangle \in \Sigma^* \times \Sigma^* \mid y \ne \text{code}(M) \text{ for any } M \text{ or } y = \text{code}(M) \text{ and } M \text{ does not halt on } x \}
$$

We use **proof by contradiction**: suppose there exists a Turing machine $M_{HC}$ that recognizes $\text{HALT}^-$. Together with a machine $M_H$ that recognizes $\text{HALT}$, we can construct the following machine $M$ decides $\text{HALT}$:

<div style="overflow-x: auto; white-space: nowrap;">
  <table style="border-spacing: 0;">
    <tr>
      <td><img src="/images/blog/halting/htm.svg" alt="HTM" width="500"/></td>
    </tr>
  </table>
</div>

The input $x$ is given to both $M_H$ and $M_{HC}$, which run in parallel. The simplest method is to let each machine execute one step at a time, alternating between them. Since $M_H$ and $M_{HC}$ recognize $\text{HALT}$ and $\text{HALT}^-$ respectively, for any $\langle y, x \rangle \in \text{HALT}$, $M_H$ will halt and accept; otherwise, $M_{HC}$ will halt and accept.

This proof idea applies to any recognizable language—in fact, the complement of any recognizable language is not recognizable.



## Conclusion

We have now proven that the Halting Problem is undecidable, and that no known real-world computational model can solve it. But how can we deal with it—or at least work around it?

The answer is to place restrictions on the Halting Problem. For example: does Turing machine $M$ halt on input $x$ within 100 steps? This version is clearly decidable.



---

**Acknowledgments**  
This blog references material from the slides of **COMP0017 Computability and Complexity Theory** at University College London.
