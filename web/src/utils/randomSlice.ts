export default function randomSlice<T>(array: T[], size: number): T[] {
    return array.slice().sort(() => Math.random() - Math.random()).slice(0, size);
}
