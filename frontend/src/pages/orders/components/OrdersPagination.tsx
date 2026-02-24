import type { ReactElement, Dispatch, SetStateAction } from "react";
import { Stack, Button } from "@mui/material";

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
  prevCursorDate,
  prevCursorId,
  nextCursorDate,
  nextCursorId,
  setCursorDate,
  setCursorId,
  setDirection,
  setCurrentPage,
}: Readonly<{
  currentPage: number;
  totalPages: number;
  setPage: Dispatch<SetStateAction<number | undefined>>;
  prevCursorDate: string | undefined;
  prevCursorId: string | undefined;
  nextCursorDate: string | undefined;
  nextCursorId: string | undefined;
  setCursorDate: Dispatch<SetStateAction<string | undefined>>;
  setCursorId: Dispatch<SetStateAction<string | undefined>>;
  setDirection: Dispatch<SetStateAction<"prev" | "next" | undefined>>;
  setCurrentPage: Dispatch<SetStateAction<number>>;
}>): ReactElement => {
  const handleCursorPagination = (direction: "prev" | "next") => {
    setDirection(direction);
    if (direction == "prev") {
      setCursorDate(prevCursorDate);
      setCursorId(prevCursorId);
      setCurrentPage(currentPage - 1);
    } else if (direction == "next") {
      setCursorDate(nextCursorDate);
      setCursorId(nextCursorId);
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
        disabled={!prevCursorDate}
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
        disabled={!nextCursorDate}
        onClick={() => handleCursorPagination("next")}
      >
        {">"}
      </Button>
    </Stack>
  );
};

export default OrdersPagination;
