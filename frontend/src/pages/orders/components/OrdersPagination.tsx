import type { ReactElement, Dispatch, SetStateAction } from "react";
import { Stack, Button } from "@mui/material";
import type { CursorState, CursorResponse } from "../types/cursor";

const OrdersNumberPagination = ({
  currentPage,
  totalPages,
  setPage,
  setCurrentPage,
}: Readonly<{
  currentPage: number;
  totalPages: number;
  setPage: Dispatch<SetStateAction<number | undefined>>;
  setCurrentPage: Dispatch<SetStateAction<number>>;
}>): ReactElement => {
  const pages = Array.from({ length: totalPages }, (_, i) => i + 1);

  const handlePageNumberPagination = (page: number) => {
    setPage(page);
    setCurrentPage(page);
  };

  return (
    <Stack direction="row" spacing={1}>
      {pages.map((page) => (
        <Button
          key={page}
          variant={page === currentPage ? "contained" : "text"}
          onClick={() => handlePageNumberPagination(page)}
        >
          {page}
        </Button>
      ))}
    </Stack>
  );
};

const OrdersPagination = ({
  currentPage,
  totalPages,
  setPage,
  cursorResponse,
  setCursorState,
  setCurrentPage,
}: Readonly<{
  currentPage: number;
  totalPages: number;
  setPage: Dispatch<SetStateAction<number | undefined>>;
  cursorResponse: CursorResponse | undefined;
  setCursorState: Dispatch<SetStateAction<CursorState | undefined>>;
  setCurrentPage: Dispatch<SetStateAction<number>>;
}>): ReactElement => {
  const handleCursorPagination = (direction: "prev" | "next") => {
    if (direction == "prev") {
      setCursorState({
        cursor: {
          cursorDate: cursorResponse?.prev.cursorDate,
          cursorId: cursorResponse?.prev.cursorId,
        },
        direction,
      });
      setCurrentPage(currentPage - 1);
    } else if (direction == "next") {
      setCursorState({
        cursor: {
          cursorDate: cursorResponse?.next.cursorDate,
          cursorId: cursorResponse?.next.cursorId,
        },
        direction: direction,
      });
      setCurrentPage(currentPage + 1);
    }
  };

  return (
    <Stack
      direction="row"
      justifyContent="center"
      alignItems="center"
      spacing={1}
    >
      <Button
        disabled={!cursorResponse?.prev.cursorDate}
        onClick={() => handleCursorPagination("prev")}
      >
        {"<"}
      </Button>
      <OrdersNumberPagination
        currentPage={currentPage}
        totalPages={totalPages}
        setPage={setPage}
        setCurrentPage={setCurrentPage}
      />
      <Button
        disabled={!cursorResponse?.next.cursorDate}
        onClick={() => handleCursorPagination("next")}
      >
        {">"}
      </Button>
    </Stack>
  );
};

export default OrdersPagination;
