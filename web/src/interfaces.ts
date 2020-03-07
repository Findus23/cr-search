export interface Person {
  "id": number;
  "name": string;
  "color": string;
}

export interface Episode {
  "episode_number": number;
  "id": number;
  "season": number;
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
