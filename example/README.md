# 工作流程

- 0.准备音频文件

    本例中使用 [example.m4a](./example.m4a) （截取自 6.S081 2020 视频教程 Lecture 1, 40s-105s）

- 1.生成文本数据

    通过语音识别，生成文本数据 [example.json](./example.json)

    ``` python
    python subtool.py audio2text -i example/example.m4a -o example/example.json
    ```

    打印日志：

    ``` log
    upload file success.
    create task success. {"TaskId": 1137614980}
    wait task complete.  {"TaskId": 1137614980, "Status": 0, "StatusStr": "waiting", "Result": "", "ErrorMsg": "", "ResultDetail": null}
    wait task complete.  {"TaskId": 1137614980, "Status": 1, "StatusStr": "doing", "Result": "", "ErrorMsg": "", "ResultDetail": null}
    get res success.
    write to example/example.json.
    ```

- 2.生成草稿字幕

    使用命令行工具生成草稿字幕文件 `example.draft.srt` （此时 `example.draft.srt` 的内容为 [example-0.draft.srt](./example-0.draft.srt) ）

    ``` python
    python subtool.py text2draft -i example/example.json -o example/example.draft.srt
    ```

- 3.校正英文字幕

    *人工校正* 英文字幕，直接编辑草稿字幕文件 `example.draft.srt` （完成后， `example.draft.srt` 的内容为 [example-1.draft.srt](./example-1.draft.srt) ）

- 4.生成中文翻译

    通过机器翻译，在草稿字幕中生成中文翻译（完成后， `example.draft.srt` 的内容为 [example-2.draft.srt](./example-2.draft.srt) ）

    ``` python
    python subtool.py en2zh -i example/example.draft.srt
    ```

    打印日志：

    ``` log
    ['Alright, I want to start by laying out some of the goals of the course.', 'So, number one is to understand design and implementation of operating systems.', 'Yeah, design is sort of high level structure and implementation is really about what the code looks like,', "and we'll be spend a lot of time with both.", "And in the interest of getting deep understanding of what's going on,", "you'll get hands on experience with a small, with a small operating system, the xv6 operating system.", 'And in addition to actually looking at an existing operating system,', "that you'll be in the labs get a bunch of experience,", 'extending the operating system, modifying, improving its behavior', 'and writing system software that it uses the operating system interfaces, [if it works an application].']
    757
    ['好的，我想从列出课程的一些目标开始。', '所以，首先要了解操作系统的设计和实现。', '是的，设计是一种高层次的结构，而实现实际上是关于代码看起来是什么样子，', '我们会花很多时间和这两个人在一起。', '为了深入了解正在发生的事情，', '您将亲身体验一个小型的、带有小型操作系统的xv6操作系统。', '除了实际查看现有的操作系统之外，', '你会在实验室里积累很多经验，', '扩展操作系统、修改、改进其行为', '以及编写使用操作系统接口的系统软件(如果它可以运行应用程序)。']
    ```

- 5.校正中文字幕

    *人工校正* 中文字幕，直接编辑草稿字幕文件 `example.draft.srt` （完成后 `example.draft.srt` 的内容为 [example-3.draft.srt](./example-3.draft.srt) ）

- 6.生成英文字幕

    使用命令行工具生成英文字幕 [example.en.srt](./example.en.srt)

    ``` python
    python subtool.py draft2final --langs en -i example/example.draft.srt -o example.en.srt
    ```

- 7.生成中文字幕

    使用命令行工具生成中文字幕 [example.zh.srt](./example.zh.srt)

    ``` python
    python subtool.py draft2final --langs en --langs zh -i example/example.draft.srt -o example.zh.srt
    ```
