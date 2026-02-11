import { Box, Typography } from "@mui/material";
import { useEffect, useState } from "react";
import axios from "axios";
import OrdersTable from "./components/OrdersTable";
import OrdersPagination from "./components/OrdersPagination";
import type { Order } from "./components/OrdersTable";

const API_URL = import.meta.env.VITE_API_URL;

type OrdersResponse = {
  orders: Order[];
  prevCursorDate: string | null;
  prevCursorId: string | null;
  nextCursorDate: string | null;
  nextCursorId: string | null;
  totalPages: number;
  currentPage: number;
  totalOrders: number;
};

export default function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [prevCursorDate, setPrevCursorDate] = useState<string>();
  const [prevCursorId, setPrevCursorId] = useState<string>();
  const [nextCursorDate, setNextCursorDate] = useState<string>();
  const [nextCursorId, setNextCursorId] = useState<string>();

  const [currentPage, setCurrentPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [totalOrders, setTotalOrders] = useState<number>(0);

  const [cursorDate, setCursorDate] = useState<string>();
  const [cursorId, setCursorId] = useState<string>();
  const [direction, setDirection] = useState<"prev" | "next">();
  const [page, setPage] = useState<number>();

  useEffect(() => {
    (async () => {
      try {
        const res = await axios.get<OrdersResponse>(`${API_URL}/orders`, {
          params: {
            page: page,
            cursorDate: cursorDate,
            cursorId: cursorId,
            direction: direction,
          },
        });
        console.log(currentPage, page, cursorDate);
        setOrders(res.data.orders);
        setPrevCursorDate(res.data.prevCursorDate ?? undefined);
        setPrevCursorId(res.data.prevCursorId ?? undefined);
        setNextCursorDate(res.data.nextCursorDate ?? undefined);
        setNextCursorId(res.data.nextCursorId ?? undefined);
        setTotalPages(res.data.totalPages);
        setTotalOrders(res.data.totalOrders);

        setCursorDate(undefined);
        setCursorId(undefined);
        setDirection(undefined);
        setPage(undefined);
      } catch (err) {
        console.error("Error fetching orders:", err);
      }
    })();
  }, [currentPage]);

  return (
    <Box>
      <Typography>Orders Page</Typography>
      <OrdersTable
        orders={orders}
        totalOrders={totalOrders}
        currentPage={currentPage}
      />
      <OrdersPagination
        currentPage={currentPage}
        totalPages={totalPages}
        setPage={setPage}
        prevCursorDate={prevCursorDate}
        prevCursorId={prevCursorId}
        nextCursorDate={nextCursorDate}
        nextCursorId={nextCursorId}
        setCursorDate={setCursorDate}
        setCursorId={setCursorId}
        setDirection={setDirection}
        setCurrentPage={setCurrentPage}
      />
    </Box>
  );
}
