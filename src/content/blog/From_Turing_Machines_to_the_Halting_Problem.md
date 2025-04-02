---
title: 'From Turing Machines to the Halting Problem'
description: 'empty'
pubDate: 'Apr 01 2025'
tags: ['computability theory', 'Turing machine']
---

## Why Turing Machines?

If you know a bit about Turing machines, you might wonder: in an era where computing devices have gone through countless iterations, the Turing machine seems like an awkward and inefficient model. Any modern device appears far more elegant and fast. So, is it still necessary to understand the Turing machine? What can it possibly offer us today?

For the first question, the answer is: it depends. If you're not interested in computability or complexity theory and your focus is purely on applications, then you might not need to study Turing machines at all.

For the second question, the Turing machine offers a formal mathematical model for rigorous proofs — and it's surprisingly powerful:

- The Church–Turing thesis tells us that any computable problem can be solved by a Turing machine. This means anything your computer can do—or anything you can program in Python, Haskell, or C—can also be done by a Turing machine. In terms of computational power, they are equivalent.

- If an algorithm runs in polynomial time on a Turing machine, it will also run in polynomial time on a RAM model—that is, on real-world devices like smartphones and computers.

Therefore, if we prove an algorithm’s complexity on the Turing machine model, it will have the same complexity class on any programming language or RAM-based device (though not exactly the same runtime). The same applies in reverse.

Moreover, if we prove that a problem cannot be solved by a Turing machine, then no programming language or any other model can solve it.

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
            <td><img src="/images/blog/halting/tm1.svg" alt="TM1" width="200"/></td>
            <td><img src="/images/common/right_arr.svg" alt="Arrow" width="50"/></td>
            <td><img src="/images/blog/halting/tm2.svg" alt="TM2" width="200"/></td>
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

For the input `11001`, the Turing machine runs on the tape as follows:
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

