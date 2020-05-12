const botui = new BotUI('bot'); // give it the id of container
botui.message.bot({ // show first message
  delay: 500,
  type: 'html',
  content: 'Hi, I\'m <b>Flow!</b>',
  loading: true // fake typing

}).
then(() => {
  return botui.message.bot({ // second one
    delay: 500,
    type: 'html',
    loading: true,
    content: "I'm here to answer questions related to COVID-19." });
}).then(() => {
  botui.message.
  bot({
    delay: 700,
    loading: true,
    content: 'How can I help you today?' }).then(() => {
      $.get('http://127.0.0.1:5000/topic/load').then(() => {
        chat()
    })
  })
});

function chat() {
  botui.action.text({
      delay: 400,
      action: {
        size: 60,
        icon: 'user-circle-o',
        sub_type: 'text',
        placeholder: 'What are the symptoms of COVID-19?' }
  }).then(res => {
    $.get('http://127.0.0.1:5000/topic/'+res.value, function(response){
      return botui.message.bot({ // second one
        delay: 500,
        loading: true,
        content: response });
      }).then(() => {
        return botui.message.bot({ // second one
          delay: 500,
          type: 'html',
          loading: true,
          content: "Did I answer your question?" })
          .then(() => {
            return botui.action.button({ // let user choose something
              delay: 300,
              action: [
              {
                text: 'Yes',
                value: 'yes' },
              {
                text: 'No',
                value: 'no' }]
            })
          }).then(function(answered) {
            if (answered.value == 'yes') {
              return botui.message.bot({ // second one
                delay: 500,
                type: 'html',
                loading: true,
                content: "Great! Is there anything else I can help you with?" })
              .then(function(){
                chat();
              })
            }
            else {
              $.get('http://127.0.0.1:5000/topic/topfivequestions/'+res.value, function(response){
                botui.message.bot({ // second one
                  delay: 500,
                  type: 'html',
                  loading: true,
                  content: "Please select one of the five questions or none of the above." });

                botui.message.bot({ // second one
                  delay: 500,
                  type: 'html',
                  loading: true,
                  content: response })
                  .then(() => {
                    question1 = response.split('<br>')[0];
                    question2 = response.split('<br>')[2];
                    question3 = response.split('<br>')[4];
                    var question4 = response.split('<br>')[6]
                    var question5 = response.split('<br>')[8]
                    return botui.action.button({ // let user choose something
                      delay: 300,
                      action: [
                      {
                        text: question1,
                        value: question1 },
                      {
                        text: question2,
                        value: question2 },
                      {
                        text: question3,
                        value: question3 },
                      {
                        text: question4,
                        value: question4 },
                      {
                        text: question5,
                        value: question5 },
                      {
                        text: 'None of the above',
                        value: 'none' }]
                    }).then(function(selection) {
                      if (selection.value != "none") {
                        $.get('http://127.0.0.1:5000/getanswer/'+selection.value, function(answer){
                          return botui.message.bot({ // second one
                            delay: 500,
                            loading: true,
                            content: answer });
                          }).then(() => {
                            return botui.message.bot({ // second one
                              delay: 500,
                              type: 'html',
                              loading: true,
                              content: "Did I answer your question?" })
                              .then(() => {
                                return botui.action.button({ // let user choose something
                                  delay: 300,
                                  action: [
                                  {
                                    text: 'Yes',
                                    value: 'yes' },
                                  {
                                    text: 'No',
                                    value: 'no' }]
                                })
                              })
                              .then(function(answer){
                                if (answer.value == 'yes') {
                                  return botui.message.bot({ // second one
                                    delay: 500,
                                    type: 'html',
                                    loading: true,
                                    content: "Great! Is there anything else I can help you with?" })
                                    .then(function(){
                                      chat();
                                    })
                                }
                              })
                            })
                      }
                      else if (selection.value == 'none') {
                        $.get('http://127.0.0.1:5000/onlinesearch/'+res.value, function(option){
                          botui.message.bot({ // second one
                            delay: 500,
                            type: 'html',
                            loading: true,
                            content: "Unfortunately, I don't have an answer for that. Check out this website for an answer to your question." });

                          return botui.message.bot({ // second one
                            delay: 500,
                            type: 'html',
                            loading: true,
                            content: option });
                          }).then(function() {
                            botui.message.bot({ // second one
                              delay: 500,
                              type: 'html',
                              loading: true,
                              content: "Is there anything else I can help you with?" });
                          }).then(function(){
                            chat();
                          })
                      }
                    })
                  })
                })
              }

          });
      })

    /*return botui.message.bot({ // second one
      delay: 500,
      loading: true,
      content: "You're asking a question related to COVID-19 symptoms; is that correct?" });*/
  })/*.then(() => {
    return botui.message.bot({ // second one
      delay: 500,
      loading: true,
      content: "The most common symptoms of COVID-19 are fever, tiredness, and dry cough. Some patients may have aches and pains, nasal congestion, runny nose, sore throat or diarrhea. These symptoms are usually mild and begin gradually." });
  })*/
}
