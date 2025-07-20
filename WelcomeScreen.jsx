import React, { useState } from 'react';
import { Search } from 'lucide-react';

const WelcomeScreen = ({ onStartChat, appName = "BCA Expert App" }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onStartChat(query);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-orange-50 flex flex-col items-center justify-center p-4">
      <div className="max-w-2xl w-full text-center">
        {/* Logo and Title */}
        <div className="mb-8">
          <div className="w-20 h-20 mx-auto mb-4 bg-blue-900 rounded-2xl flex items-center justify-center">
            <img 
              src="/logo.jpg" 
              alt="BCA Expert App Logo" 
              className="w-16 h-16 object-contain rounded-xl"
            />
          </div>
          <h1 className="text-4xl font-bold text-blue-900 mb-2">{appName}</h1>
          <p className="text-gray-600 text-lg">
            Your expert guide to the Building Code of Australia
          </p>
        </div>

        {/* Search Input */}
        <form onSubmit={handleSubmit} className="mb-8">
          <div className="relative max-w-lg mx-auto">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Type your question..."
              className="w-full pl-10 pr-4 py-3 border-2 border-green-300 rounded-lg focus:outline-none focus:border-green-500 text-lg"
            />
          </div>
        </form>

        {/* Footer */}
        <div className="mt-12 text-sm text-gray-500">
          Based on the National Construction Code (NCC) 2022
        </div>
      </div>
    </div>
  );
};

export default WelcomeScreen;

