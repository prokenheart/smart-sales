import { Button, Typography, Stack } from "@mui/material";
import { useEffect, useState, type ReactElement } from "react";

import OrdersTable from "@orders/components/OrdersTable";
import OrdersPagination from "@orders/components/OrdersPagination";
import OrderForm from "@orders/components/OrderForm";
import SearchBox from "@orders/components/SearchBox";

import { OrderRefreshContext } from "@orders/context/OrderRefreshContext";

import type { CursorResponse, CursorState } from "@orders/types/cursor";
import type { Order } from "@orders/types/order";

import { getOrders } from "@services/order";

const OrdersPage = (): ReactElement => {
  const [orders, setOrders] = useState<Order[]>([]);

  const [cursorResponse, setCursorResponse] = useState<CursorResponse | null>(
    null
  );

  const [currentPage, setCurrentPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);

  const [totalOrders, setTotalOrders] = useState<number>(0);
  const [ordersPerPage, setOrdersPerPage] = useState<number>(1);

  const [page, setPage] = useState<number | null>(null);

  const [cursorState, setCursorState] = useState<CursorState>({
    cursor: {
      cursorDate: null,
      cursorId: null,
    },
    direction: null,
  });

  const [isOpenForm, setIsOpenForm] = useState(false);

  const [shouldRefreshOrder, setShouldRefreshOrder] = useState(false);

  const [search, setSearch] = useState<string>("");

  const handleCreateOrder = () => {
    setIsOpenForm(true);
  };

  const fetchOrders = async () => {
    const res = await getOrders(
      page,
      cursorState?.cursor.cursorDate,
      cursorState?.cursor.cursorId,
      cursorState?.direction,
      search
    );

    setOrders(res.data.orders);
    if (res.data) {
      setCursorResponse({
        prev: {
          cursorDate: res.data.prevCursorDate,
          cursorId: res.data.prevCursorId,
        },
        next: {
          cursorDate: res.data.nextCursorDate,
          cursorId: res.data.nextCursorId,
        },
      });
    }

    setTotalPages(res.data.totalPages);
    setTotalOrders(res.data.totalOrders);
    setOrdersPerPage(res.data.ordersPerPage);

    setCursorState({
      cursor: {
        cursorDate: null,
        cursorId: null,
      },
      direction: null,
    });
    setPage(null);
  };

  useEffect(() => {
    fetchOrders();
  }, [currentPage]);

  useEffect(() => {
    if (currentPage === 1) fetchOrders();
    else setCurrentPage(1);
  }, [search]);

  useEffect(() => {
    if (shouldRefreshOrder) {
      setIsOpenForm(false);
      setShouldRefreshOrder(false);
      if (currentPage === 1) fetchOrders();
      else setCurrentPage(1);
    }
  }, [shouldRefreshOrder]);

  return (
    <>
      <Stack
        direction="row"
        justifyContent="space-between"
        alignItems="center"
        mb={2}
      >
        <Typography variant="h5">Orders</Typography>

        <Stack direction="row" spacing={2} alignItems="center">
          <SearchBox value={search} onChange={setSearch} delay={500} />
          <Button variant="contained" onClick={handleCreateOrder}>
            Add Order
          </Button>
        </Stack>

        <OrderRefreshContext.Provider value={{ setShouldRefreshOrder }}>
          <OrderForm isOpen={isOpenForm} setIsOpen={setIsOpenForm} mode="create" />
        </OrderRefreshContext.Provider>
      </Stack>

      <OrdersTable
        orders={orders}
        totalOrders={totalOrders}
        currentPage={currentPage}
        ordersPerPage={ordersPerPage}
        setOrders={setOrders}
      />
      <OrdersPagination
        currentPage={currentPage}
        totalPages={totalPages}
        setPage={setPage}
        cursorResponse={cursorResponse}
        setCursorState={setCursorState}
        setCurrentPage={setCurrentPage}
      />
    </>
  );
};

export default OrdersPage;
