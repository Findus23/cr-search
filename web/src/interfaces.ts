export interface Person {
  "id": number;
  "name": string;
  "color": string;
}

export interface Series {
  "id": number;
  "is_campaign": boolean;
  "single_speaker": boolean;
  "title": string;
  "slug": string;
}

export interface SeriesData extends Series {
  "last_upload": string;
  "length": number;
}

export interface Episode {
  "episode_number": number;
  "id": number;
  "series": Series;
  "pretty_title": string;
  "video_number": number;
  "youtube_id": string;
}

export interface Line {
  "id": number;
  "order": number;
  "ismeta": boolean;
  "isnote": boolean;
  "starttime": number;
  "endtime": number;
  "text": string;
  "person": Person | null;
  "episode": Episode;
}

export interface Result {
  "resultID": number;
  "centerID": number;
  "offset": number;
  "lines": Line[];
}

export interface ServerMessage {
  status: string;
  message: string;
}

export interface ServerData {
  "series": SeriesData[];
}

export interface EpisodeDetailed extends Episode {
  "downloaded": boolean;
  "text_imported": boolean;
  "phrases_imported": boolean;
  "upload_date": string;
}

export interface SeriesData {
  "meta": Series;
  "episodes": EpisodeDetailed[];
}
