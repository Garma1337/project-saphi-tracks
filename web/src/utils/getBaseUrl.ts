export default function getBaseUrl() {
    return window.location.href.replace(window.location.pathname, '');
}
