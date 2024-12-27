import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const ProductionGraph = () => {
  // Get the data from the window object where we'll store it in the template
  const data = window.productionData || [];

  return (
    <div className="w-full h-64 bg-white rounded-lg shadow-sm p-4">
      <h3 className="text-lg font-semibold mb-4">Milk Production Trend</h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="date" 
            tick={{ fontSize: 12 }}
          />
          <YAxis 
            tick={{ fontSize: 12 }}
            label={{ 
              value: 'Liters', 
              angle: -90, 
              position: 'insideLeft',
              fontSize: 12 
            }} 
          />
          <Tooltip />
          <Line 
            type="monotone" 
            dataKey="total" 
            stroke="#2563eb" 
            strokeWidth={2}
            dot={{ fill: '#2563eb' }} 
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ProductionGraph;
