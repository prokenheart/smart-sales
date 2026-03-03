import { Autocomplete, TextField } from "@mui/material";
import { useEffect, useState } from "react";
import type { Dispatch, ReactElement, SetStateAction } from "react";

import type { Customer } from "@orders/types/order";

import { searchCustomers } from "@/services/customer";

const CustomerSelect = ({
  selectedCustomer,
  setSelectedCustomer,
}: Readonly<{
  selectedCustomer: Customer | undefined;
  setSelectedCustomer: Dispatch<SetStateAction<Customer | undefined>>;
}>): ReactElement => {
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
      const res = await searchCustomers(debouncedKeyword);

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
        <TextField {...params} label="Select Customer" size="small" />
      )}
      isOptionEqualToValue={(option, value) =>
        option.customerId === value.customerId
      }
      fullWidth
    />
  );
};

export default CustomerSelect;
