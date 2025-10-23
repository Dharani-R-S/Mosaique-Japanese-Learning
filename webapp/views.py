from django.shortcuts import render, redirect
from django.urls import reverse

LESSONS = [
    {'id': 1, 'title': 'Hiragana Basics', 'subtitle': 'Learn あ い う', 'progress': 30, 'color': 'pink'},
    {'id': 2, 'title': 'Katakana Intro', 'subtitle': 'Learn カ キ ク', 'progress': 60, 'color': 'aqua'},
    {'id': 3, 'title': 'JLPT N5 Kanji', 'subtitle': '10 essential kanji', 'progress': 10, 'color': 'mint'},
    {'id': 4, 'title': 'Particles 101', 'subtitle': 'は が を に で', 'progress': 0, 'color': 'peach'},
]


def home(request):
    quick = [
        {'title': 'Kanji', 'url': reverse('webapp:kanji', args=['N5'])},
        {'title': 'TalkMate', 'url': reverse('webapp:talkmate', args=['N5'])},
        {'title': 'Listening', 'url': reverse('webapp:listening', args=['N5'])},
        {'title': 'Reading', 'url': reverse('webapp:reading', args=['N5'])},
    ]
    context = {'lessons': LESSONS, 'quick': quick}
    return render(request, 'webapp/home.html', context)


def lessons(request):
    context = {'lessons': LESSONS}
    return render(request, 'webapp/lessons.html', context)


def lesson_detail(request, pk):
    lesson = next((l for l in LESSONS if l['id'] == pk), None)
    if not lesson:
        return render(request, 'webapp/lesson_detail.html', {'error': 'Lesson not found'})
    return render(request, 'webapp/lesson_detail.html', {'lesson': lesson})


def kanji(request, level='N5'):
    kanji_list = [
        {'char': '日', 'meaning': 'sun/day', 'onyomi': 'ニチ, ジツ', 'kunyomi': 'ひ, -び, -か', 'example': '日本 (にほん) — Japan'},
        {'char': '人', 'meaning': 'person', 'onyomi': 'ジン, ニン', 'kunyomi': 'ひと', 'example': '一人 (ひとり) — one person'},
        {'char': '口', 'meaning': 'mouth', 'onyomi': 'コウ, ク', 'kunyomi': 'くち', 'example': '入口 (いりぐち) — entrance'},
        {'char': '山', 'meaning': 'mountain', 'onyomi': 'サン', 'kunyomi': 'やま', 'example': '富士山 (ふじさん) — Mt. Fuji'},
    ]
    context = {'level': level, 'kanji_list': kanji_list, 'progress': 20}
    return render(request, 'webapp/kanji_section.html', context)


def talkmate(request, level='N5'):
    default_messages = [
        {'role': 'assistant', 'text': 'こんにちは！今日は何を勉強しますか？'},
        {'role': 'user', 'text': '私は日本語を勉強しています。'},
        {'role': 'assistant', 'text': 'いいですね！今日の目標は何ですか？'},
    ]
    messages = request.session.get('talk_messages', default_messages.copy())

    if request.method == 'POST':
        user_input = request.POST.get('user_input', '').strip()
        if user_input:
            messages.append({'role': 'user', 'text': user_input})
            messages.append({'role': 'assistant', 'text': '（この応答はモックです）いいですね！続けてください。'})
            request.session['talk_messages'] = messages
            return redirect(reverse('webapp:talkmate', args=[level]))

    return render(request, 'webapp/talkmate.html', {'level': level, 'messages': messages})


def listening(request, level='N5', unit='1'):
    audio_list = [
        {
            'id': 1,
            'title': 'Daily Greeting',
            'duration': 28,
            'speaker': 'A & B',
            'difficulty': 'Beginner',
            'file': 'webapp/audio/sample1.mp3',
            'question': 'What did the speaker say about the weather?',
            'options': ['It was sunny', 'It rained', 'It snowed', 'It was cloudy']
        },
        {
            'id': 2,
            'title': 'At the Station',
            'duration': 35,
            'speaker': 'A & B',
            'difficulty': 'Beginner',
            'file': 'webapp/audio/sample1.mp3',
            'question': 'Which platform should they go to?',
            'options': ['Platform 2', 'Platform 3', 'Platform 5', 'Platform 1']
        },
        {
            'id': 3,
            'title': 'In the Restaurant',
            'duration': 42,
            'speaker': 'Waiter & Customer',
            'difficulty': 'Intermediate',
            'file': 'webapp/audio/sample1.mp3',
            'question': 'What did the customer order?',
            'options': ['Ramen', 'Sushi', 'Curry rice', 'Tempura']
        },
    ]

    context = {'level': level, 'unit': unit, 'audio_list': audio_list}
    return render(request, 'webapp/listening.html', context)


def reading(request, level='N5'):
    readings = [
        {'title': 'Short convo', 'japanese': '今日はいい天気ですね。散歩しましょう。', 'english': 'The weather is nice today. Let’s go for a walk.'},
        {'title': 'At the store', 'japanese': 'このりんごはいくらですか？', 'english': 'How much is this apple?'},
    ]
    return render(request, 'webapp/reading.html', {'level': level, 'readings': readings})


def jlpt_test(request, level='N5'):
    questions = [
        {'question': 'Choose the correct particle: 私 __ 学校 に 行きます。', 'options': ['は', 'が', 'を', 'に']},
        {'question': 'What is the meaning of 「猫」?', 'options': ['dog', 'cat', 'bird', 'fish']},
        {'question': 'Which is Hiragana for "ka"?', 'options': ['か', 'カ', 'き', 'く']},
    ]

    if request.method == 'POST':
        correct_indexes = [0, 1, 0]
        total = len(questions)
        correct = 0
        details = []

        for idx in range(total):
            qname = f"q{idx+1}"
            selected = request.POST.get(qname)
            try:
                sel_index = int(selected)
            except (TypeError, ValueError):
                sel_index = None

            is_correct = (sel_index == correct_indexes[idx])
            if is_correct:
                correct += 1

            details.append({
                'question': questions[idx]['question'],
                'selected': sel_index,
                'correct_index': correct_indexes[idx],
                'is_correct': is_correct,
                'options': questions[idx]['options'],
            })

        percent = round((correct / total) * 100) if total else 0
        result = {'total': total, 'correct': correct, 'percent': percent, 'details': details}

        return render(request, 'webapp/jlpt_test.html', {
            'level': level,
            'questions': questions,
            'time_limit': 10,
            'result': result,
        })

    return render(request, 'webapp/jlpt_test.html', {'level': level, 'questions': questions, 'time_limit': 10})
