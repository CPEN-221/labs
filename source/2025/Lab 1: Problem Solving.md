# Lab 1: Problem Solving

This lab assignment involves solving a few computational problems to make you comfortable with some standard programming structures (especially iteration).

**You will submit your work on PrairieLearn.**

> During the lab sessions, the teaching assistants will advise on problem solving and will introduce you to the use of `git`, which is the source code control system that we will use. You will obtain the source code for one of the problems using GitHub Classroom and then you should attempt a solution and *push* your work to GitHub.

For this lab activity, we *will not* grade you on the basis of whether you submitted your work to GitHub or not. You will have to use `git` and GitHub as we move ahead with the course so it is essential that you get comfortable with these tools.

---

> For Fall 2024, this lab activity involves three programming problems:

1. > Wireless Signal Strength (straightforward computation);
2. > String Chopping (discussed as Lab 0 but was not graded then);
3. > Addition Closure.

# Wireless Signal Strength

The strength of a wireless channel is measured in decibels, and the strength changes as the distance between the transmitter and the receiver increases. There are [several different models](http://www.wirelesscommunication.nl/reference/contents.htm#propagation) for the signal strength of a channel but we will use one of the simplest models. If the initial signal strength is $s$ decibels and the distance between the transmitter is $d $  metres then the received signal strength is

```math
r = s \times \left( \sum_{i=1}^{n} {a_i}d^{x_i} \right).
```

One can represent the model using an array `coefficients` (coefficients of the polynomial in the model) and an array `exponents` (exponents of the polynomial). The lengths of `coefficients` and `exponents` will be the same. Given `s`, `coefficients`, `exponents` and `d`, implement a method that computes `r`. For this exercise, you may assume that all inputs used for testing will be valid (e.g., no `null` inputs will be used).

## Examples

1. `s = 10`, `a = {5, 4}`, `x = {-1, 0}`, `d = 10`: `r = 45`.
2. `s = 100`, `a = {100}`, `x = {-2}`, `d = 13`: `r = 59.1715976331361`.
3. `s = 5`, `a = {-1, 20}`, `x = {1, 0}`, `d = 25`: `r = -25.0` (some models are not realistic!).

# String Chopping

In Edwardian England, the punishment of [drawn, hanged and quartered](https://en.wikipedia.org/wiki/Hanged,_drawn_and_quartered) was the common penalty for treason. This activity involves nothing as grisly; here we are merely chopping up parts of a string.

For a `String` `s`, we can refer the first third of a `s` as its **head**, the last third of it as its **tail** and the remaining characters as its **middle**.

If `l` is the length of a `String`, then let `t = ceiling(l/3)` represent the length of the head and tail. The **ceiling** of a non-integer value `x` is the smallest integer `c` such that `c >= x`. `ceiling(4.3)` is `5`. `ceiling(5)` is `5`.

For the `String` `"marathon"`, the head is `"mar"`, the middle is `"at"`, and the tail is `"hon"`.

One can chop a string by removing its head, middle or tail. Chopping off the head of `"marathon"` gives us the `String` `"athon"`. Chopping off the tail of `"marathon"` gives us the `String` `"marat"`, and chopping the middle gives us `"marhon"`.

We will use `h` or `H` to denote chopping off the head of a string, `t` or `T` for chopping off the tail, and `m` or `M` for chopping off the middle.

We can dice `"marathon"` to the single character `t` using the chop sequence `"THHH"`, which represents the following sequence of chops: `"marathon" -> "marat" -> "rat" -> "at" -> 't'`.

The end goal of this activity is to develop a program that determines, for each letter of the alphabet, the chopping sequence that allows us to obtain that letter from a given string.

> ## Examples

1. > Input: `"x"`; Output: `{"NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "", "NO", "NO"}`. We do not need to chop the string to obtain `'x'`.
2. > Input: `"qwertyuiopasdfghjkl"`; Output: `{"HTHMTT", "NO", "NO", "HHTMTH", "MTMHTT", "HHTHMT", "HHHMTT", "HHHMTH", "HTTMTT", "HHHHMT", "HHHHHT", "HHHHHH", "NO", "NO", "HTTMTH", "HTTHMT", "MTMTTT", "MTHTTT", "HHTMTT", "MTHTTH", "MHMTTH", "NO", "MTMTTH", "NO", "MHMTTT", "NO"}`.
3. > Input: `"aaaaaaaaaaaaaaaaaabaaaaaaaaaaaaaaaa"`; Output: `{"HHHHHHH", "HMHTTTT", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO"}`

# Addition Closure

You are given a `List` of `Integer`s, `listInt`, and another integer `n`. We will define *closure under addition* for `listInt` to mean that for *any* two distinct values of `i` and `j`, `(listInt[i]+listInt[j]) % n` is in `listInt` or `k * n + (listInt[i]+listInt[j]) % n` (for some int `k`) is in `listInt`.

Your goal is to determine if a given `List` of `Integer`s is closed under addition for some modulus `n`. You will implement a method, *isClosed*, that will return `true` if a `List` is closed under addition for a given `n` and `false` otherwise.

> ## Examples

> #### input list: [-1, 0, 1]; `n` = 2

- > Returns: `true`
- > `(-1 + 0) % 2 = -1; (-1 + 1) % 2 = 0, (0 + 1) % 2 = 1`.

> #### input list: [-2, 3]; `n` = 4

- > Returns: `false`

> #### input list: [1, 1, 0]; `n` = 2

- > Returns: `true`

> #### input list: [1, 1]; `n` = 3

- > Returns: `false`

> #### input list: [1, 1, 2]; `n` = 2

- > Returns: `true`

> #### input list: [0, 1, 1, 2]; `n` = 2

- > Returns: `true`

> #### input list: [0, 1, 100, 50, 50], `n` = 100

- > Return: `false`

> #### input list: [0, 1, 100, 50, 50], `n` = 50

- > Return: `true`
