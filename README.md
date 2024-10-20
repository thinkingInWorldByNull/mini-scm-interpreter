# mini-scm-interpreter

> 说明：为什么要开发一套语言？不同层的技术问题有着不同的语言原语从而屏蔽细节，对上提供更好的抽象。比如汇编语言面对的是如何用简单的指令对二进制进
> 行封装对应的源语就是操作寄存器、内存相关的，而对高级语言来说，面对的是如何提供更高的抽象让程序员专注于业务问题屏蔽平台细节，因此每一层的语言
> 都在尽力提供自己的一套词汇从而方便问题的划分和归一。总之从这个角度来看，程序员不再仅仅是会使用咒语的魔法师还应该是语言的设计师。
> **思想表达的核心局限性核心在于思想而不是语言的层面**。


本解释器`Mini-SCM-Interpreter` 基于《计算机程序的构造和解释》的元语言抽象写出，目的在于更好的理解语言，解开语言背后的面纱。

- [x] : Token和语法树解析
- [x] : 增加 `Eval-Apply` 结构
- [x] : 支持内置函数比如`max`, `min`...
- [x] : 支持Lambda
- [x] : 支持Macro和简单宏展开
- [x] : 惰性求值
- [x] : 执行和计算分离

## Token和语法树解析

### Token解析

解析Token的过程在于把字符串转变为可以被解释器【这里是Python】解释的符号比如

- `#t` 解析为`True`
- `"3.14"` 解析为 `3.14`
- `age` 解析为名称标识符`age`

Token解析可以归纳为从左往右扫描token符号并应用解析规则识别，详细的规则参考`Tokenizer._TOKEN_TYPE_EXTRACT_RULE`。

**扫描符号**

- 如果是注释符号则跳过
- 遇到空白跳过
- 记录单个分隔符`()'`则记录该token和位置
- 对其他表示符号名称等截取该位置到最近的一个空白符或则分隔符为止比如`max(a,b)`对`max`而言需要解析到`(`的位置

**识别Token值**

将解析规则应用于解析的token符号，核心过程如下

```python
def _gen_token_stream(self, line: str):
    """解析token，丢弃空白文本和注释"""
    token, next_token_idx = _next_candidate_token(line, 0)

    while token:
        if (res := self._extract_token(token)) is not None:
            yield res
        else:
            _raise_token_value_exception(line, token, next_token_idx)
        token, next_token_idx = _next_candidate_token(line, next_token_idx)
```

### 语法树解析

`lisp`的语法天然贴合语法树的表示比如`(define (abs x) (if (< x 0) (- x) x ) )`对应的语法树示意图如下。


```
┌───────┬───┐     ┌─────┬────┐          ┌───┬────┐                                                  
│ define│ . ┼─────┤ .   │ .  ├────────► │ . │ nil│                                                  
└───────┴───┘     └─┬───┴────┘          └─┬─┴────┘                                                  
                    │                     │                                                         
                    ▼                     ▼                                                         
                  ┌─────┬────┐          ┌─────┬────┐       ┌───┬────┐      ┌───┬────┐     ┌───┬────┐
                  │abs  │ .  │          │ if  │ .  ├─────► │.  │ .  │ ────►│.  │  . │ ──► │ x │nil │
                  └─────┴─┬──┘          └─────┴────┘       └─┬─┴────┘      └─┬─┴────┘     └───┴────┘
                          │                                  ▼               │                      
                       ┌──▼─┬─────┐                        ┌────┬───┐      ┌─▼──┬───┐               
                       │  x │ nil │                        │ <  │ . │      │ -  │ . │               
                       └────┴─────┘                        └────┴─┬─┘      └────┴─┬─┘               
                                                                  │               │                 
                                                                  │               │                 
                                                                 ┌▼─┬─────┐      ┌▼─┬─────┐         
                                                                 │x │  .  │      │x │ nil │         
                                                                 └──┴──┬──┘      └──┴─────┘         
                                                                       │                            
                                                                       ▼                            
                                                                      ┌──┬──────┐                   
                                                                      │0 │ nill │                   
                                                                      └──┴──────┘                                                                                                                          
```

解析规则将token流分为二部分，一部分为expr处理解析对象，指针部分由rest解析。

对expr来说处理能够被直接解析的部分
- 遇到`(`则返回rest部分
- 遇到`nil`则返回nil对象
- 遇到符号则返回符号
- 遇到引用则构建一个引用pair然后继续调用expr递归解析

对rest函数而言负责递归构建`Pair(expr(), rest()))`,结束条件为遇到了终止符`)`则认为本次解析结束，具体解析参考`Parser.parser()`

这样一个代表语法树的解析完成，接下来开始支持最核心的功能`Eval-Apply`结构

## Eval-Apply

> ❗️一切要从转变思路开始，写下的符号的作用取决于你如何解释！

## 从一个简单的例子说明元循环求值器

思考一个问题，`(+ 1 2)`是如何工作的？首先将`(`和`)`识别为环境，然后找到操作符`+`对数字`1 2`进行操作。这里有一个比较重要的问题那就是如何从环
境中找到`+`的操作语义的。

工作示意图如下

```
           Env                        
      ┌──────────────┐                
      │              │                
      │  (+(1 2))    │        ┌──┬──┐ 
      │      + ◄─────┼────────┤1 │2 │ 
      │              │        └──┴──┘ 
      └──────────────┘                
             ▲                        
             │                        
    ┌────────┴────────┐               
Body│(define (+) ...) │               
    └─────────────────┘               
```

从图来看，求值器的工作就是将数字`1 2`引导到操作符`+`从而返回结果，这里又引出一个很奇妙的问题从效果来看是查询`+`的操作过程然后将参数应用该过程。
这样伪代码类似如下

``` python
def find_producer(op_id, env) -> Produce:
    pass

def eval(expr, env):
    ...
    find_producer(get_op_id(expr), env)(get_args(expr))   
    ...
```

但是仔细思考一下发现**查询的过程本身也是求值的过程**，这时候**问题就变成了如何对给定的序列依次求值**，再来看表达式`(+ 1 2)`。就可以看做

- 求值 `+`,返回的结果应该是一个过程实现`+`的语义
- 求值 `1`返回`1`
- 求值 `2`返回`2`
- 对`(+ 1 2)`求值就是将数字`1 2`应用到`+`过程的结果

## 考虑一个稍微复杂的例子

从上面的例子中得出思考，求值的过程本身就是具有自解释性的，重点在于如何把一个较为复杂的求值引导和规划到基本求值过程中。

但是这里我们并没有对写出来的代码给出更加新奇的解释。现在考虑下面的代码

```lisp
(define (square x) (* x x))
(square (+ 1 2))
```

对`(define (square x) (* x x))`而言求值顺序为
1. 找到`define`过程对`(square x) (* x x)`求值，返回lambda过程类似`lambda (x) (* x x)`
2. 找到`lambda`过程对`(x) (* x x)`求值，这个过程包括解析形参列表`(x)`， 过程体`(* x x)`，然后将`square`绑定和lambda过程绑定到环境

对`(square (+ 1 2))`求值
1. 对`square`求值，返回lambed过程
2. 对`(+ 1 2)`请值
   - 对`+`求值
   - 应用参数`1 2`
   - 整体求值得到`3`
3. 用`3`将表达式`(square (+ 1 2))`替换成`(square 3)`
4. `(square 3)`整体求值
   - 对x参数和3绑定到新环境
   - 在新环境中对过程体`(* x x)`求值
   - 得到`9`

从中可以看到求值其实由二部分定义 —— `evaluate = eval + apply`，简而言之求值就是不断细化到可以被直接处理的规划然后不断应用求值的过程。从这个
角度来看我们写的代码`(define (square x) (* x x))`，也能够得出另一番理解那就是**我们的代码其实就是对一个大问题的拆分和下层求值逻辑的规划**。

上面的过程大致如下

```
    Env_1                          Env_2        
┌─────────────┐                                     
│             │                 ┌──────────┐        
│    square   │◄────────────────┤  x=3     │        
│      ▲      │                 │          │        
└──────┼──────┘                 └────▲─────┘        
       │                             │               
┌──────┴───────┐                 (square 3) =(* x x)
│ param:x      │                            =(* 3 3)
│ body: (* x x)│                                    
└──────────────┘                                    
```


















