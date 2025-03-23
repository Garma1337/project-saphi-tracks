export default function getYouTubeVideoCode(videoUrl: string): string | null {
    const videoCode = videoUrl.split('v=')[1]

    if (!videoCode) {
        return null;
    }

    const ampersandPosition = videoCode.indexOf('&')
    if (ampersandPosition !== -1) {
        return videoCode.substring(0, ampersandPosition)
    }

    return videoCode
}
