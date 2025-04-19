import { useState } from 'react';
import './App.css';

function App() {
  const [level, setLevel] = useState('');
  const [start, setStart] = useState(false);

  const handleStart = () => {
    if (level) setStart(true);
    else alert("Please select your level first!");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 to-purple-100 flex items-center justify-center p-4">
      <div className="bg-white shadow-xl rounded-2xl p-8 w-full max-w-md text-center">
        <h1 className="text-3xl font-bold mb-4 text-gray-800">English Quiz</h1>
        <p className="text-gray-600 mb-6">Test your English skills based on your level</p>

        {!start ? (
          <>
            <select
              value={level}
              onChange={(e) => setLevel(e.target.value)}
              className="w-full mb-4 px-4 py-2 border rounded-xl text-gray-700"
            >
              <option value="">Select level</option>
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
            <button
              onClick={handleStart}
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded-xl w-full transition"
            >
              Start Quiz
            </button>
          </>
        ) : (
          <div className="text-green-600 font-semibold text-lg">
            🚀 Starting quiz for <span className="capitalize">{level}</span> level...
          </div>
        )}
      </div>
    </div>
  );
}

export default App;