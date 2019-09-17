---
title: 'Hello, world!'
subtitle: 'An introduction to this world.'
date: '2019-09-17'
author: 'Aleksander B. Birkeland'
alternative-author: 'thebirk'
...

#### A test!

#### A title with a random class {.the_random_class}

Here is some text.

Less text. ASDas

#### Some LaTeX math

$$\frac{a}{b}$$

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
