import {expect, test } from "vitest";
import getYouTubeVideoCode from "./getYouTubeVideoCode.ts";

test('can get youtube video code from url', () => {
    const url = 'https://www.youtube.com/watch?v=Aw32Nbwk47Q';
    const videoCode = getYouTubeVideoCode(url);
    expect(videoCode).toBe('Aw32Nbwk47Q');
})

test('can get youtube video code from url with extra parameters', () => {
    const url = 'https://www.youtube.com/watch?v=Aw32Nbwk47Q&feature=youtu.be';
    const videoCode = getYouTubeVideoCode(url);
    expect(videoCode).toBe('Aw32Nbwk47Q');
})

test('can not get youtube video code if invalid video url', () => {
    const url = 'https://www.youtube.com/watch';
    const videoCode = getYouTubeVideoCode(url);
    expect(videoCode).toBe(null);
})
