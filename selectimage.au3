WinWaitActive("Выгрузка файла")
Send("c:\default.png")
;Send($CmdLine[1])
ControlClick("Выгрузка файла", "Open", 1)