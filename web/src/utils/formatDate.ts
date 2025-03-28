export default function formatDate(time: string) {
    let date = new Date(time);

    const offset = date.getTimezoneOffset()
    date = new Date(date.getTime() - (offset * 60 * 1000))

    const hour =  ('0' + (date.getHours())).slice(-2);
    const minute =  ('0' + (date.getMinutes())).slice(-2);
    const seconds = ('0' + (date.getSeconds())).slice(-2);

    return date.toISOString().split('T')[0] + ' ' + hour + ':' + minute + ':' + seconds;
}
