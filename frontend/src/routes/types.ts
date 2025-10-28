import { z } from 'zod/v4';

export const submitSchema = z.object({
    source: z.enum(['discogs', 'spotify']).default('discogs'),
    link: z.url('Неверная ссылка.'),
    username: z.string().min(1, 'Никнейм не должен быть пустым.')
});

export const rankingSchema = z.object({
    username: z.string().min(1, 'Никнейм не должен быть пустым.'),
    placements: z.int().array()
});

export class Track {
    album_id: number;
    track_name: string;
    id: number;
    constructor() {
        this.album_id = 1;
        this.track_name = "Magic Window";
        this.id = 1;
    }
}

export class Album {
    id: number;
    name: string;
    artist: string;
    duration: string
    cover: string;
    total_tracks: number;
    constructor() {
        this.id = 1;
        this.name = "Geogaddi";
        this.artist = "Boards Of Canada";
        this.duration = '01:05:55'
        this.total_tracks = 23;
        this.cover = "https://i.discogs.com/bmfLrSi2cDLqYCPMbZoju2i4rB-RtIhEdVVUGmCaTYI/rs:fit/g:sm/q:90/h:600/w:595/czM6Ly9kaXNjb2dz/LWRhdGFiYXNlLWlt/YWdlcy9SLTI0NDMy/LTEyMTE1Njk3MDku/anBlZw.jpeg";
    }
}

export class Rankings {
    username: string;
    placement: number;
    constructor() {
        this.username = "Joosenitsa"
        this.placement = 1
    }
}

export class Ranking {
    track_name: string;
    rankings: Rankings[];
    placement: number;
    constructor() {
        this.track_name = "Magic Window"
        this.rankings = [new Rankings]
        this.placement = 1
    }
}

export class TGUser {
    id: number;
    username?: string;
    photo_url?: string;
    first_name: string;
    last_name?: string;
    auth_date: number;
    hash: string;
    constructor() {
        this.id = 1
        this.first_name = "Ivan"
        this.auth_date = 1
        this.hash = ""
    }
};