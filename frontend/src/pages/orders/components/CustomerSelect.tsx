import { Autocomplete, TextField } from "@mui/material";
import axios from "axios";
import { useEffect, useState, type Dispatch, type SetStateAction } from "react";
import type { Customer } from "../types/order";

const API_URL = import.meta.env.VITE_API_URL;

export default function CustomerSelect({
  selectedCustomer,
  setSelectedCustomer,
}: Readonly<{
  selectedCustomer: Customer | undefined;
  setSelectedCustomer: Dispatch<SetStateAction<Customer | undefined>>;
}>) {
  const [customers, setCustomers] = useState<Customer[]>([]);

  const [keyword, setKeyword] = useState("");
  const [debouncedKeyword, setDebouncedKeyword] = useState("");

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedKeyword(keyword);
    }, 400);

    return () => clearTimeout(timer);
  }, [keyword]);


  useEffect(() => {
    if (!debouncedKeyword.trim()) {
      setCustomers([]);
      return;
    }

    const fetchCustomers = async () => {
      const res = await axios.get<Customer[]>(
        `${API_URL}/customers?query=${debouncedKeyword}`
      );

      setCustomers(res.data);
    };

    fetchCustomers();
  }, [debouncedKeyword]);

  return (
    <Autocomplete
      options={customers}
      value={selectedCustomer ?? null}
      onChange={(_, newValue) => setSelectedCustomer(newValue ?? undefined)}
      getOptionLabel={(option) =>
        `${option.customerName} - ${option.customerPhone}`
      }
      onInputChange={(_, value) => setKeyword(value)}
      renderInput={(params) => (
        <TextField {...params} label="Search Customer" size="small" />
      )}
      isOptionEqualToValue={(option, value) =>
        option.customerId === value.customerId
      }
    />
  );
}
