# pyfck - python using only 8 characters: exc'%=()

This repo outlines a method of encoding any python script using only the following 8 characters:

`e x c ' % = ( )`


# History of fuck

Way back in 1993, Urban Müller created the esoteric programming language [Brainfuck](https://en.wikipedia.org/wiki/Brainfuck),
which is a turing complete (but essentially unreadable) programming language that can be written with only 6 characters (`+-<>[]`).

Some time later in 2009, Yosuke Hasegawa created what would eventually become [JSFuck](https://en.wikipedia.org/wiki/JSFuck), a way of writing valid JavaScript code using only 18 characters.
Over the next year, this would be reduced down to just 6 characters (`[]()!+`). I'm pretty sure this was actually my first exposure to any kind of esoteric programming when I started learning to program in JS around 2015.

This would inevitably inspire the repo [pyfuck](https://github.com/wanqizhu/pyfuck), which in 2017 would get python3 down to only 13 characters (`[(+travels')]`).
In 2022, a [fork of pyfuck](https://github.com/Samdaaman/pyfuck) reduced the python3 limit down to just 9 characters (`exc'=()%+`).

Technically, the pyfuck fork was inspired by a [stackexchange post](https://codegolf.stackexchange.com/a/110677) from early 2017 (before the original pyfuck repo)
that outlined how to write python3 using the same 9 characters, so really the first person to hit 9 was probably some random stackoverflow codegolfer.
However, their method grows exponentially with the number of characters in the encoding program, so the 2022 fork (which grows linearly) is arguably an improvement.

Now in 2023, for some reason I wasted half a day and managed to to remove one more character from the 9 character python3 pyfuck limit.
Introducing pyfck!
Valid python3 code using only 8 characters (`exc'%=()`).


# Method


## Getting strings from numbers

The core strategy involves using up 5 characters (`exc()`) to get the ability to use the python builtin `exec` function, which lets you execute arbitrary python code given the program in string form.

This first step in achieving this is to add the characters `'` (single quote) and `%` (percent), which gives us access to string formatting.

Using `%c` and either `+` or `,`, we can now get arbitrary strings if we have the equivalent ascii integer representation for each character.

```python3
# spaces can be removed with no effect
'%c' % 104 + '%c' % 105 = 'hi'  
'%c%c' % (104,105) = 'hi'
```

Since `%%` will format to the `%` literal, we can actually remove the need for either a comma `,` or plus `+` using the following technique.

```python3
'%c%%c' % 104 % 105 = 'hi`
```

This works because the string is passed through multiple formatting executions. The first will convert the `%c` to `h`, and the `%%` to `%`, giving the string `h%c`. The second will then replace with `%c` with `i`, giving `hi`.

Unfortunately, by removing that additional character our encoding method grows exponentially with the number characters in the target string, but I suppose this is just the price we pay for saving a single byte.

The string "hi fren!" now looks something like this and has over 250 characters.
``` python3
# Paste this into a python interpreter to get the 8 character string "hi fren!"
'%c%%c%%%%c%%%%%%%%c%%%%%%%%%%%%%%%%c%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%c%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%c%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%c' % 104 % 105 % 32 % 102 % 114 % 101 % 110 % 33
```



## Getting numbers from hell

Now comes the tricky part (yes, strings from numbers was child's play).

So far we have used 7 characters `exc()%'`, and the goal is to get access to all integers in as few extra characters as possible.

Previous methods achieved this with 2 extra characters:
 - `1` and `+`, which allows you to chain addition to reach any integer `1+1+1+...` (`1%1` can be used for `0`). [Source](https://codegolf.stackexchange.com/a/110677).
 - `=` and `+`, which allows you to chain addition, where `1` is achieved via truthiness (`''==''`). This method lets you avoid exponential encoding growth. [Source](https://github.com/Samdaaman/pyfuck).

The pyfck method manages to get all integers using only a single extra character (`=`).


### 0 and 1

Similar to the 9 character method, we can use the expressions `(''=='')` to get `True` and `(''==())` to get `False`.
To work towards all possible integers, we would like to access these in digit form (i.e. `0` and `1`).

A key insight is that we actually have access to more methods of string formatting than `%c`.
Since we are already including `x` from `exec`, we can use `%x` which is for hexadecimal string formatting (i.e. take an integer, convert to its hexadecimal string).

```python3
# a string with bytes 0 and 1
'%c' % (''==()) = '%c' % False = '\x00'
'%c' % (''=='') = '%c' % True = '\x01'

# 0 and 1 in string form
'%x' % (''==()) = '%x' % False = '0'
'%x' % (''=='') = '%x' % True = '1'
```


### Give me 🅱️

We now put all our efforts into reaching the string `'b'`.

Fortunately, hexadecimal string formatting is capable of producing exactly 6 letters, one of which is `b`.
In fact, `b` is the hexadecimal encoding of 11, which is itself made of only 1's!

This means the python expression `'%x' % 11 = 'b'` will evaluate to the string `'b'`.

Using the string formatting method outlined before, we can get the string `'11'` like so:
```python3
# Note this gives the string '11', not the integer 11 which is what we wanted
'%x%%x' % (''=='') % (''=='')
-> '%x%%x' % True % True
-> '1%x' % True
-> '11'
```

So close! We just need to cast this to an integer. Thankfully we have a total of `0` characters remaining to achieve this.

Alternatively, we can try assigning the integer 11 to a variable.
How? Well what if we `exec` the string `x=11`.

```python3
exec('x=%x%%x' % (''=='') % (''==''))
-> exec('x=%x%%x' % True % True)
-> exec('x=1%x' % True)
-> exec('x=11')
-> x=11  # this variable now exists and equals 11, if only we could access it...
```


### exec again

To access `x`, we can't run multiple statements in a single `exec` without additional characters like newlines or semicolons `;` to separate statements.
We can however try running `exec` again, and if we ensure that the `exec` runs only after the first exec that sets `x=11`, we should be able to use `x`.

One method of achieving this is by using the fact that python lets you chain equalities statements.

When you evaluate a statement like `f() == g() == h()` python will lazily evaluate left to right, first comparing `f()` to `g()`, and then comparing `g()` to `h()`.
If any value is different (e.g. `f()==1` and `g()==2`), python will not execute `h()` for efficiency reasons (no point comparing `g()` with `h()` if we already know the entire equality will evalute to `False`).

Fortunately for us `exec()` will always return `None`, so we can chain together `exec()` statements and execute them left to right like so:
```python3
# This will print 11 and then 22
exec('x=11') == exec('print(x)') == exec('x=22') == exec('print(x)')
```


### Binary!

The more attentive of you may have noticed my desire for `b` was actually because I was trying to use Python's binary syntax that lets you express any integer using only `0`, `1` and `b`.
For example, we can express the integer `2` in python using `0b10`.

If we place `exec('x=11')` to the left, we can now abuse string formatting techniques and assign variables to arbitrary digits.
```python3
exec('x=11') == exec('xx=%x%%x%%%%x%%%%%%%%x' % (''==()) % x % (''=='') % (''==()))
-> x=11; exec('xx=%x%%x%%%%x%%%%%%%%x' % (''==()) % x % (''=='') % (''==()))
-> x=11; exec('xx=%x%%x%%%%x%%%%%%%%x' % True % 11 % True % False)
-> x=11; exec('xx=0%x%%x%%%%x' % 11 % True % False)
-> x=11; exec('xx=0b%x%%x' % True % False)
-> x=11; exec('xx=0b1%x' % False)
-> x=11; exec('xx=0b10')
-> x=11; xx=0b10
-> x=11; xx=2  # the variable "ce" now exists and equals 2 for all execs to the right
```

Now if we just chain enough of these `exec` variable assignments with unique(!) variable names, we should be able to access any integer.




### Program Execution

Using the original string from digits method, we can now represent (and execute) any string by just assigning all the needed binary integers to variables in `exec` statements to the left.

Consider the python program `c=8`.

We have the following ascii to digit conversions:
 - `ord('c') = 99 = 0b1100011`
 - `ord('=') = 61 = 0b111000`
 - `ord('8') = 56 = 0b111101`

We then exec the following statements in order:
```python3
x = 11                # Needed to access the string 'b'
eecccee = 0b1100011   # Store the digit for 'c' in variable `eecccee`
eeeccc = 0b111000     # Store the digit for '=' in variable `eeeccc`
eeeece = 0b111101     # Store the digit for '8' in variable `eeeece`
```

Notice how in order to prevent variable name collisions and massively ballooning variable name sizes (e.g. `x=1, xx=2, xxx=3, ...`),
we construct variable names by replacing `0` with `c` and `1` with `e` in its binary form (recall both `c` and `e` are in our 8 character set).

Our final `exec` statement can then use the variables `eecccee`, `eeeccc`, `eeeece` to construct and execute the string `c=8`.

```python3
exec('%c%%c%%%%c' % eecccee % eeeece % eeeccc)
-> exec('%c%%c%%%%c' % 99 % 61 % 56)
-> exec('c%c%%c' % 61 % 56)
-> exec('c=%c' % 56)
-> exec('c=8')
-> c=8
```


# Examples


### Smallest program
One of the smallest valid python programs that isn't just an expression uses only 3 characters in regular form, but when converted to our 8 character form requires 1377 characters.

**Original**
```python
c=8
```

**New**
```python
exec('x=%x%%x'%(''=='')%(''==''))==exec('eeeece=%x%%x%%%%x%%%%%%%%x%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x'%(''==())%x%(''=='')%(''=='')%(''=='')%(''=='')%(''==())%(''==''))==exec('eecccee=%x%%x%%%%x%%%%%%%%x%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x'%(''==())%x%(''=='')%(''=='')%(''==())%(''==())%(''==())%(''=='')%(''==''))==exec('eeeccc=%x%%x%%%%x%%%%%%%%x%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x'%(''==())%x%(''=='')%(''=='')%(''=='')%(''==())%(''==())%(''==()))==exec('%c%%c%%%%c'%eecccee%eeeece%eeeccc)
```

### Hello World
The standard hello world python program is 22 characters normally and ~4.2 million characters in `pyfck` form. So instead I have added an example of a simpler program which prints just "Hi!" at a much more reasonable 9293 characters.

**Original**
```python
print("Hi!")
```

**New** (and improved)
```python
exec('x=%x%%x'%(''=='')%(''==''))==exec('ececce=%x%%x%%%%x%%%%%%%%x%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x'%(''==())%x%(''=='')%(''==())%(''=='')%(''==())%(''==())%(''==''))==exec('ecccec=%x%%x%%%%x%%%%%%%%x%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x'%(''==())%x%(''=='')%(''==())%(''==())%(''==())%(''=='')%(''==()))==exec('ecccce=%x%%x%%%%x%%%%%%%%x%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x'%(''==())%x%(''=='')%(''==())%(''==())%(''==())%(''==())%(''==''))==exec('eeecccc=%x%%x%%%%x%%%%%%%%x%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x'%(''==())%x%(''=='')%(''=='')%(''=='')%(''==())%(''==())%(''==())%(''==()))==exec('eeececc=%x%%x%%%%x%%%%%%%%x%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x'%(''==())%x%(''=='')%(''=='')%(''=='')%(''==())%(''=='')%(''==())%(''==()))==exec('ececcc=%x%%x%%%%x%%%%%%%%x%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x'%(''==())%x%(''=='')%(''==())%(''=='')%(''==())%(''==())%(''==()))==exec('ecceccc=%x%%x%%%%x%%%%%%%%x%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x'%(''==())%x%(''=='')%(''==())%(''==())%(''=='')%(''==())%(''==())%(''==()))==exec('eeceeec=%x%%x%%%%x%%%%%%%%x%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x'%(''==())%x%(''=='')%(''=='')%(''==())%(''=='')%(''=='')%(''=='')%(''==()))==exec('eececce=%x%%x%%%%x%%%%%%%%x%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x'%(''==())%x%(''=='')%(''=='')%(''==())%(''=='')%(''==())%(''==())%(''==''))==exec('eeeccec=%x%%x%%%%x%%%%%%%%x%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x'%(''==())%x%(''=='')%(''=='')%(''=='')%(''==())%(''==())%(''=='')%(''==()))==exec('%c%%c%%%%c%%%%%%%%c%%%%%%%%%%%%%%%%c%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%c%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%c%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%c%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%c%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%c%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%c%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%c'%eeecccc%eeeccec%eececce%eeceeec%eeececc%ececcc%ecccec%ecceccc%eececce%ecccce%ecccec%ececce)
```



# Future Work


## Program Size

The current version of `pyfck` grows exponentially with the input program.

If anyone can figure out how to reduce the asymptotic growth rate to below $O(2^n)$ I think that would be an objective improvement.

A couple potential non-asymptotic ways to reduce program size could be:
 - Using the first 2 `exec` statements to assigns variables `xe` and `xc` to `True` and `False`. Then your formatting chains will looks like `...%xe%xc%xc%...` instead of `...%(''==())%(''==())%(''==())%...`.
 - Using early `exec`s to assign variables to a large number of `%`'s. Then substitute these strings as needed, perhaps by getting access to `s` (`'%c' % 115`) and using `%s` string substitution.


One potential asymptotic method is to run an `exec` before the final program `exec` which defines a variable/function that can be used to avoid the long format string (`%c%%c%%%%c...`) for the program.
Maybe a lambda that helps you construct that format string, or avoid it entirely using tuples?



## Character Set

I honestly have no idea how you would go about getting to 7 characters without major technique changes.

If you can get access to an integer like `1` and remove 2 other characters, you *might* be able use modulus (`%`) and the `e` operator to get all relevant ascii integers.
Some interesting results I found earlier:
```
0 = 1%1
1 = 1
2.0 = 1e111 % 111 % 11
3.0 = 1e111 % 1e11 % 11
4.0 = 1e111 % 1e11 % 1111 % 1e1
5.0 = 1e111 % 1111 % 111
6.0 = 1e111 % 111 % (1e111 % 1e11 % 111)
7.0 = 1e111 % 1e11 % 111 % 11
8.0 = 1e111 % 1e11 % 111 % 1e1
9.0 = 1e111 % 11111 % 11
10.0 = 1e1
...
```

Many of these are floats unfortunately, so you would need to figure out how to cast to int also...


At this point I think the easiest way to lose another character is to wait for future Python version and pray.




