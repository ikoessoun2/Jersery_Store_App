
import "./index.css"
import { useState } from "react"

function App() {

  const [count, setCount] = useState<number>(0);
  const handleIncrement = (): void => {
    setCount(count + 1);
  };

  const handleDecrement = (): void => {
    setCount(count - 1);
  };

  return (
    <main className="">
      <h1 className="text-4xl font-bold text-red-600">
        Jersey Store
      
      </h1>

      <div className="flex items-center justify-center gap-4">
        <button
          className="px-4 py-2 text-white bg-blue-500 rounded hover:bg-blue-600"
          onClick={handleDecrement}
        >
          -
        </button>
        <span className="text-xl">{count}</span>
        <button
          className="px-4 py-2 text-white bg-blue-500 rounded hover:bg-blue-600"
          onClick={handleIncrement}
        >
          +
        </button>
      </div>
    </main>
  )
}

export default App
