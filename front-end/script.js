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
    content: 'How can I help you today?' }).

  then(() => {
    chat()
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
  }).then(() => {
    return botui.message.bot({ // second one
      delay: 500,
      loading: true,
      content: "You're asking a question related to COVID-19 symptoms; is that correct?" });
  }).then(() => {
    return botui.action.button({ // let user choose something
      delay: 300,
      action: [
      {
        text: 'Yes',
        value: 'yes' },
      {
        text: 'No',
        value: 'no' }] });
  }).then(() => {
    return botui.message.bot({ // second one
      delay: 500,
      loading: true,
      content: "The most common symptoms of COVID-19 are fever, tiredness, and dry cough. Some patients may have aches and pains, nasal congestion, runny nose, sore throat or diarrhea. These symptoms are usually mild and begin gradually." });
  }).then(() => {
    chat();
  })
}
