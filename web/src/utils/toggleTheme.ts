import getCurrentTheme from "./getCurrentTheme.ts";

const toggleTheme = () => {
    const newTheme = getCurrentTheme() === 'light' ? 'dark' : 'light';
    localStorage.setItem('theme', newTheme);

    window.location.reload();
}

export default toggleTheme;