// static/script.js

function getBotResponse() {
    let rawText = document.getElementById("textInput").value;
    let userHtml = '<div class="userText"><span>' + rawText + '</span></div>';
    document.getElementById("textInput").value = "";
    document.getElementById("chatbox").innerHTML += userHtml;
    document.getElementById("chatbox").scrollTop = document.getElementById("chatbox").scrollHeight;
    fetch(`/get?msg=${rawText}`)
        .then(response => response.json())
        .then(data => {
            if (data.questions.length === 0) {
                let botHtml = '<div class="botText"><span>すいません。データが見つかりません。</span></div>';
                document.getElementById("chatbox").innerHTML += botHtml;
            } else {
                let botHtml = '<div class="botText"><span>以下から選択してください:</span><ul>';
                data.questions.forEach((item, index) => {
                    botHtml += `<li class="botOptions" onclick="selectAnswer(${data.ids[index]}, '${item}')">${item}</li>`;
                });
                botHtml += `<li class="botOptions" onclick="selectAnswer(-1, 'ここにはない')">ここにはない</li>`;
                botHtml += '</ul></div>';
                document.getElementById("chatbox").innerHTML += botHtml;
            }
            document.getElementById("chatbox").scrollTop = document.getElementById("chatbox").scrollHeight;
        });
}

function selectAnswer(id, questionText) {
    // First, display the selected question as if the user has typed it
    let userHtml = '<div class="userText"><span>' + questionText + '</span></div>';
    document.getElementById("chatbox").innerHTML += userHtml;
    document.getElementById("chatbox").scrollTop = document.getElementById("chatbox").scrollHeight;
    // Next, fetch and display the answer to the selected question
    fetchAnswer(id);
}

function fetchAnswer(id) {
    if (id == -1) {
        let botHtml = '<div class="botText"><span>それについては情報が見つかりませんでした。他の質問はありますか？</span></div>';
        document.getElementById("chatbox").innerHTML += botHtml;
        document.getElementById("chatbox").scrollTop = document.getElementById("chatbox").scrollHeight;
    } else {
        fetch(`/get_answer?id=${id}`)
            .then(response => response.json())
            .then(data => {
                let botHtml = '<div class="botText"><span>' + data.answer + '</span></div>';
                document.getElementById("chatbox").innerHTML += botHtml;
                document.getElementById("chatbox").scrollTop = document.getElementById("chatbox").scrollHeight;
            });
    }
}



let isComposing = false;

document.getElementById("textInput").addEventListener("compositionstart", function(e) {
    isComposing = true;
});

document.getElementById("textInput").addEventListener("compositionend", function(e) {
    isComposing = false;
});

document.getElementById("textInput").addEventListener("keydown", function(e) {
    if (!isComposing && e.code === "Enter" && !e.shiftKey && document.activeElement === document.getElementById("textInput")) {
        e.preventDefault();
        document.getElementById("buttonInput").click();
    }
});