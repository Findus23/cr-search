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
  "person": Person;
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

export interface SeriesNames {
  "id": number;
  "title": string;
}

export interface ServerData {
  "series": SeriesNames[];
}

export interface EpisodeDetailed extends Episode {
  "downloaded": boolean;
  "text_imported": boolean;
  "phrases_imported": boolean;
}

export interface SeriesData {
  "meta": Series;
  "episodes": EpisodeDetailed[];
}
