export type CursorState = {
	cursor: Cursor;
  direction: "prev" | "next" | null;
};

type Cursor = {
  cursorDate: string | null;
  cursorId: string | null;
};

export type CursorResponse = {
	prev: Cursor;
	next: Cursor;
}
