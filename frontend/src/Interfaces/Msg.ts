export interface Msg {
  who: "me" | "bot";
  msg: string;
  time: string;
  status: "sent" | "read";
}
