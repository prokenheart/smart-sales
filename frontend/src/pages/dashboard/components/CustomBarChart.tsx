import type { ReactElement } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid } from "recharts";

type ChartData = {
  key: string;
  value: number;
};

export const CustomBarChart = ({
  data,
}: Readonly<{ data: ChartData[] }>): ReactElement => {
  const top5 = data.slice(0, 5);

  const getYAxisWidth = (data: { key: string }[]) => {
    const maxLength = Math.max(...data.map((d) => d.key.length));
    return maxLength * 8; 
  };

  return (
    <BarChart height={300} data={top5} layout="vertical">
      <CartesianGrid strokeDasharray="3 3" />

      <XAxis type="number"  />

      <YAxis type="category" dataKey="key" interval={0} width={getYAxisWidth(data)}/>

      <Bar
        dataKey="value"
        fill="#f9b17a"
      />
    </BarChart>
  );
};
