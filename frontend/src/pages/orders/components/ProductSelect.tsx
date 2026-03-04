import { Autocomplete, TextField } from "@mui/material";
import { useEffect, useState } from "react";
import type { Dispatch, ReactElement, SetStateAction } from "react";

import type { Product } from "@orders/types/product";

import { searchProducts } from "@/services/product";

const ProductSelect = ({
  selectedProduct,
  setSelectedProduct,
}: Readonly<{
  selectedProduct: Product | undefined;
  setSelectedProduct: Dispatch<SetStateAction<Product | undefined>>;
}>): ReactElement => {
  const [products, setProducts] = useState<Product[]>([]);

  const [keyword, setKeyword] = useState("");
  const [debouncedKeyword, setDebouncedKeyword] = useState("");

  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedKeyword(keyword);
    }, 400);

    return () => clearTimeout(timer);
  }, [keyword]);

  useEffect(() => {
    if (!debouncedKeyword.trim()) {
      setProducts([]);
      return;
    }

    const fetchProducts = async () => {
      try {
        setIsLoading(true);
        const res = await searchProducts(debouncedKeyword);
        setProducts(res.data);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProducts();
  }, [debouncedKeyword]);

  return (
    <Autocomplete
      options={products}
      loading={isLoading}
      value={selectedProduct ?? null}
      onChange={(_, newValue) => setSelectedProduct(newValue ?? undefined)}
      getOptionLabel={(option) => option.productName}
      onInputChange={(_, value) => setKeyword(value)}
      renderOption={(props, option) => (
        <li {...props}>
          {option.productName} - {option.prices[0].priceAmount}
        </li>
      )}
      renderInput={(params) => (
        <TextField {...params} label="Select Product" size="small" />
      )}
      noOptionsText={
        keyword.trim() === "" ? "Type to search product" : "No products found"
      }
      loadingText="Finding product..."
      isOptionEqualToValue={(option, value) =>
        option.productId === value.productId
      }
    />
  );
};

export default ProductSelect;
