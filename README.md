# Билеты к экзамену

## Дедлайн до 10.01.23 23:59

## Если у меня есть вопросы или что-то не получается?

Напишите в чате нашей группы. Мы попытаемся оперативно помочь

## Как внести вклад?

Надо создать ветку от текущей версии данного репозитория. (* TODO)

Поправить нужные файлы. Сделать pull request вашей ветки. 

|  Предмет  | расположение файлов |  Первая буква для ветки |
| ------------ | ------------ | ------------ |
|  Линейная алгебра |  course-1/linear-algebra/question*.tex  | l |
|  Математический анализ   | course-1/mathematical-analysis/question*.tex  | m |

Название ветки должно иметь вид {первая буква предмета}{номер билета}.

Название pull request'а в гитхабе должны иметь информативное название. Например, `Добавлен билет 5 (матан)`, или `Исправил описки в билетах 2(матан), 6 (линал)`.

## Как редактировать `.tex`

[LaTeX](https://ru.wikipedia.org/wiki/LaTeX "LaTeX")

Рекомендую использовать редактор [texstudio](https://www.texstudio.org/ "texstudio").

Как установить tex? Чтобы у вас точно работала надо установить что-то по типу latex-full. В зависимости от OS будет отличаться установка. У меня на малинке друга устанавливалось минут 15.

Синтаксис проще простого. Пишем формулы вот так: `$ax^2 + bx + c = 0$` или как вы хотите, ограниячений нет. Если вы не знаете как написать то или иное в формуле то просто гуглите по типу: `latex math symbol cancel`. Можете воспользоваться редакторами онлайн, например, [редактор](https://latex.codecogs.com/eqneditor/editor.php "редактор").




## Как компилить файл? 

Во первых если вы в редакторе на подобие texstudio зайдёте в exam.tex нужного предмета, то если нажать `F5` (сборка файла) то всё будет компилиться. Не пугайтесь, что в первый раз у вас будет не очень быстро работать и вообще может не быть оглавления (в таком случае надо ещё раз запустить, это никакая не ошибка, это некоторая особенность сборки).

Или просто воспользуйтесь скриптом который лежит в корне репозитория запустив его `python3 build.py`. Если не передавать ничего то будет просто сборка всех `exam.tex`. Но при запуске  `python3 build.py linal` соберётся динал, аналогично при запуске `python3 build.py matan`.

* передайте дополнительно t что-бы запустить сборку два раза
