---
title: 'Hello, world!'
subtitle: 'An introduction to this world.'
date: '2019-09-17'
author: 'Aleksander B. Birkeland'
custom-style:
  - '
    div.the-custom-class h4 {
      color: #0aa;
    }
    '
---

#### A test!

Hello

[Home?](/)

| Name          | Age |
|:--------------|----:|
| Ola Nordmann  |  42 |
| Kari Nordmann |  24 |

#### A title with a custom class {.the-custom-class}

Here is some text.

Less text. ASDas

#### Some LaTeX

$$
\binom{a}{b} \neq  \frac{a}{b} \label{a}\tag{1}
$$
$$
\binom{a}{b} = 1 + \frac{a}{b} \label{b}\tag{2}
$$

And perhaps some inline LaTeX $y = 3x^2 + 4$.

Also here is that equation above referenced $\ref{a}$. And the second line $\ref{b}$.

#### A short list of stuff

Here is a short list of stuff for those of you who might be interested.

- Apples
- Pears
- Horses?

#### Some quotes

> Last time we spoke I introduced the concept of headers
> 
> > This is what I chose to call a header. "# This is my header"

#### A short code block

Here is an amazing code snippet.

```c++
#include <stdio.h>

template<typename T>
struct Array {
	T *data;
	size_t capacity;
	size_t size;

	T& operator[](size_t index) {
		return data[index];
	}
};

int main(int argc, char **argv) {
    printf("Hello, world!\n");
    return 0;
}
```

Here is another snippet

```
This snippet features no syntax highlighting.
```