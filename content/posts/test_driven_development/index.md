---
title: 'Test Driven Development'
date: '2024-12-13T15:52:46+01:00'
draft: false
summary: ''
tags: ["test"]
categories: []
cover:
  image: ''
  alt: ''
  caption: ''
images: []
---
We all know that person that always asks for unit tests on your Pull Request. You curse under your breath wondering why they have nothing better to do than ruining your day.

Unit tests let you know if your codebase is behaving as expected. As long as you’ve written good tests, you can be happy your codebase is healthy if tests are showing _green_. Any time a test appears in _red_, you will know that you’ve introduced a bug and you can fix it before it hits production.

There are different types of tests we can run on our applications. Unit tests are one of them, and consist on on testing your code at the smallest possible level, such as the function level. If your functions are well scoped, your unit tests can simply ensure that your code and functions are behaving as expected. Test Driven Development (TDD) is a type of unit testing where you write your tests before you start writing your code.

On the other hand TDD goes beyond unit testing. It gives you a framework where you have to think about the design of your code before you actually implement it. It forces you to think about what’s the input and what’s the output before you’ve even started writing code.

_Unit tests should be simple_

Good unit tests are those that test a single unit of code. Simple unit tests are usually a sign of a well written codebase. If a unit test is simple it means that the function it tests is well scoped and doing only one thing which makes it easy to read and test. If your unit test starts to look like it needs its own unit tests, you’ve probably found a _code smell_ that the function that is being tested needs to be refactored into smaller or better scoped functions.

When you write your code before your tests, you might accidentally write a function that tries to do too many things. When you go ahead and write your test, you realise the test you need to write is not as simple as you expected, which forces you to refactor your function so it can be easily tested.

With TDD you are forced to define the input and output of the function beforehand. It forcers you to think of what that function is designed to do. You are forced to write the input and output manually, which forces you to think about the expected functionality. When you write your test first, you are giving yourself a framework that forces you to write a function that fits that simple unit test you just wrote!

_Run Tests Often_

Another benefit of TDD is that it forces you to run tests often. An extreme but useful example often used in front end development is to automatically run unit tests every time you save a file. The benefits of this is twofold: tests for which the code has not been implemented will fail until the code or function is complete. The unit tests will give you debug information of what is breaking each time giving you a better idea on what to tackle next. Its like like constantly running a debugger.

The other benefit, is that if you are running your entire test suite, and suddenly a test that shouldn’t be failing, _fails_, you know exactly at which point in time the test failed, giving you a clearer idea of which line of code was the culprit for this. If you are waiting until the end to write your test, it will be a surprise that that other random test is failing and you’ll have to spend more time debugging why.

_Test Driven Development (TDD) gives you better quality tests_

There is also a more subtle difference why TDD gives you better quality tests. When you write unit tests after you’ve written your code, you could end up writing a test to pass your code, rather than writing a test to test your code functionality. When you write a code after the fact, you might be biased to write a code based on the current functionality of the function, rather than on the expected functionality. In other words, are you _writing a useful test that checks the function is doing what it should do_ or are you _writing a test to pass_.

## Closing words
Let’s be realistic though, TDD takes discipline. Some real world projects don’t have easy setups to run tests, and some tests might be too slow to run often. If this is the case, it is likely a _code smell_ indicating that you need a better local setup, or that some of your tests need to be refactored or moved to integration tests or e2e tests (but that’s for another post)

TDD provides a framework for writing code that is well designed, properly scoped, and easily testable. Even if you decide not to continue writing tests later on, having developed familiarity with TDD still offers a useful guide for creating code that remains straightforward to test. So, is it worth your time?

---
## My Newsletter

I send out an email every so often about cool stuff I'm building or working on.

{{< subscribe >}}
