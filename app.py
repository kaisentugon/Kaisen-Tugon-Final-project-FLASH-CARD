from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Store flashcards in a list of dictionaries
flashcards = []

@app.route('/')
def home():
    return render_template('index.html', flashcards=flashcards)

@app.route('/add', methods=['GET', 'POST'])
def add_flashcard():
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        flashcards.append({'question': question, 'answer': answer})
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_flashcard(index):
    if request.method == 'POST':
        flashcards[index]['question'] = request.form['question']
        flashcards[index]['answer'] = request.form['answer']
        return redirect(url_for('home'))
    return render_template('edit.html', flashcard=flashcards[index], index=index)

@app.route('/delete/<int:index>')
def delete_flashcard(index):
    flashcards.pop(index)
    return redirect(url_for('home'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if not flashcards:
        return redirect(url_for('home'))

    current_card = flashcards[0]  # Show the first card in the list
    show_answer = False  # By default, don't show the answer
    feedback = None  # Feedback message for the user's answer

    if request.method == 'POST':
        user_answer = request.form.get('user_answer').strip().lower()  # Normalize user input
        correct_answer = current_card['answer'].strip().lower()  # Normalize correct answer

        if user_answer == correct_answer:
            feedback = "Correct! 🎉"
        else:
            feedback = f"Incorrect. The correct answer is: {current_card['answer']}."

        flashcards.append(flashcards.pop(0))  # Move the current card to the end of the list
        show_answer = True

        return render_template('quiz.html', flashcard=current_card, show_answer=show_answer, feedback=feedback)

    return render_template('quiz.html', flashcard=current_card, show_answer=show_answer, feedback=feedback)



if __name__ == '__main__':
    app.run(debug=True)
