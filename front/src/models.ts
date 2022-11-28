export interface IDevice {
    on: boolean;
    status_wifi: boolean;
    temp: number;
    temperature: number;
    brightness: number;
    thermostat: string;
    controls_locked: boolean;
    id: number;
    serial_number: number;
    owner_id: number;
}

export interface IOwner {
    id: number;
    email: string;
    username: string;
    first_name: string;
    last_name: string;
}

export interface IChapter {
    id:number;
    title: string;
    notes: number[];
    docfiles: number[];
}

export interface INote {
    id:number;
    title: string;
    text: string;
    note_type: string;
    color: string;
    created_at: string;
    updated_at: string;
    author: IOwner;
    docfile: string;
}

export interface IImage {
    id: number;
    path: string;
}

export interface IDocfile{
    id:number;
    title: string;
    chapter: number;
    subchapter?: string;
    part?: string;
    book?: number;
    code?: string;
    version?: number;
    notes?: INote[];
    updated_at: string;
}

export interface ListServerResponse<T> {
    total_count: number;
    links?: {
        next?: string,
        previous?: string,
    }
    results: {
        count: number,
        items: T;
    }
}