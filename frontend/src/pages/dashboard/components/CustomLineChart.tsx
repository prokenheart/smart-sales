import type { ReactElement } from "react";
import { LineChart, Tooltip, Line, XAxis, YAxis} from "recharts";

type ChartData = {
  key: string;
  value: number;
};

export const CustomLineChart = ({
  data,
}: Readonly<{ data: ChartData[] }>): ReactElement => {
  return (
    <LineChart width={500} height={300} data={data}>
      <YAxis tickFormatter={(value) => `$${value}`} width="auto" />
      <XAxis dataKey="key" />

      <Tooltip />
      <Line
        type="monotone"
        dataKey="value"
        stroke="#2d3250"
        strokeWidth={2}
        dot={false}
      />
    </LineChart>
  );
};
