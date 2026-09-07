# Lab 0: String Chopping

> In Edwardian England, the punishment of [drawn, hanged and quartered](https://en.wikipedia.org/wiki/Hanged,_drawn_and_quartered) was the common penalty for treason. This activity involves nothing as grisly; here we are merely chopping up parts of a string.

### Overview

For a `String` `s`, we can refer the first third of a `s` as its **head**, the last third of it as its **tail** and the remaining characters as its **middle**.

If `l` is the length of a `String`, then let `t = ceiling(l/3)` represent the length of the head and tail. The **ceiling** of a non-integer value `x` is the smallest integer `c` such that `c >= x`. `ceiling(4.3)` is `5`. `ceiling(5)` is `5`.

For the `String` `"marathon"`, the head is `"mar"`, the middle is `"at"`, and the tail is `"hon"`.

One can chop a string by removing its head, middle or tail. Chopping off the head of `"marathon"` gives us the `String` `"athon"`. Chopping off the tail of `"marathon"` gives us the `String` `"marat"`, and chopping the middle gives us `"marhon"`.

We will use `h` or `H` to denote chopping off the head of a string, `t` or `T` for chopping off the tail, and `m` or `M` for chopping off the middle.

We can dice `"marathon"` to the single character `t` using the chop sequence `"THHH"`, which represents the following sequence of chops: `"marathon" -> "marat" -> "rat" -> "at" -> 't'`.

The end goal of this activity is to develop a program that determines, for each letter of the alphabet, the chopping sequence that allows us to obtain that letter from a given string.

> ### Examples

1. > Input: `"x"`;
Output: `{"NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "", "NO", "NO"}`. We do not need to chop the string to obtain `'x'`.
2. > Input: `"qwertyuiopasdfghjkl"`;
Output: `{"HTHMTT", "NO", "NO", "HHTMTH", "MTMHTT", "HHTHMT", "HHHMTT", "HHHMTH", "HTTMTT", "HHHHMT", "HHHHHT", "HHHHHH", "NO", "NO", "HTTMTH", "HTTHMT", "MTMTTT", "MTHTTT", "HHTMTT", "MTHTTH", "MHMTTH", "NO", "MTMTTH", "NO", "MHMTTT", "NO"}`.
3. > Input: `"aaaaaaaaaaaaaaaaaabaaaaaaaaaaaaaaaa"`;
Output: `{"HHHHHHH", "HMHTTTT", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO"}`
