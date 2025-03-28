const getCurrentTheme = () => {
    if (!localStorage.getItem('theme')) {
        localStorage.setItem('theme', 'light');
    }

    return localStorage.getItem('theme') == 'dark' ? 'dark' : 'light';
}

export default getCurrentTheme;