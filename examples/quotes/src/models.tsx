export interface Meta {
  id: string;
  score: number;
}

export interface Quote {
  meta: Meta;
  quote: string;
  author: string;
  tags: string[];
};

export interface Tag {
  tag: string;
  count: number;
};
