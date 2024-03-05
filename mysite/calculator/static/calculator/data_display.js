const dataContainer = document.querySelector('.dataContainer');

dataContainer.addEventListener('click', () => {
    const button = dataContainer.querySelector('button');
    const message = dataContainer.querySelector('div');

    button.style.display = 'none';
    message.style.display = 'block';
})