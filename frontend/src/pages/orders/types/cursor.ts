export type CursorState = {
	cursor: Cursor;
  direction: "prev" | "next" | undefined;
};

type Cursor = {
  cursorDate: string | undefined;
  cursorId: string | undefined;
};

export type CursorResponse = {
	prev: Cursor;
	next: Cursor;
}
