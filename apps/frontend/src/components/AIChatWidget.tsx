'use client';

import { useState, useRef, useEffect } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Icons } from './icons';
import { cn } from '../lib/utils';
import { useMutation } from '@apollo/client';
import { SEND_CHAT_MESSAGE } from '../lib/graphql/mutations';

type Message = {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
};

export function AIChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const [sendMessage] = useMutation(SEND_CHAT_MESSAGE);

  const handleSendMessage = async () => {
    if (!input.trim()) return;
    
    const userMessage: Message = {
      id: Date.now().toString(),
      content: input,
      role: 'user',
      timestamp: new Date(),
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    
    try {
      const { data } = await sendMessage({
        variables: { content: input },
      });
      
      const aiMessage: Message = {
        id: Date.now().toString(),
        content: data.sendChatMessage.content,
        role: 'assistant',
        timestamp: new Date(),
      };
      
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {isOpen ? (
        <div className="w-80 h-[500px] bg-white dark:bg-gray-800 rounded-lg shadow-xl flex flex-col border border-gray-200 dark:border-gray-700">
          <div className="p-4 bg-loomi-primary text-white rounded-t-lg flex justify-between items-center">
            <h3 className="font-bold">Loomi AI Assistant</h3>
            <button onClick={() => setIsOpen(false)}>
              <Icons.close className="h-4 w-4" />
            </button>
          </div>
          
          <div className="flex-1 p-4 overflow-y-auto">
            {messages.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-center text-gray-500">
                <Icons.bot className="h-8 w-8 mb-2" />
                <p>How can I help you today?</p>
              </div>
            ) : (
              <div className="space-y-4">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={cn(
                      'flex',
                      message.role === 'user' ? 'justify-end' : 'justify-start'
                    )}
                  >
                    <div
                      className={cn(
                        'max-w-xs p-3 rounded-lg',
                        message.role === 'user'
                          ? 'bg-loomi-primary text-white'
                          : 'bg-gray-100 dark:bg-gray-700'
                      )}
                    >
                      <p>{message.content}</p>
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 dark:bg-gray-700 p-3 rounded-lg">
                      <Icons.loader className="h-4 w-4 animate-spin" />
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>
          
          <div className="p-4 border-t border-gray-200 dark:border-gray-700">
            <div className="flex gap-2">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type your message..."
                onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
              />
              <Button onClick={handleSendMessage} disabled={isLoading}>
                {isLoading ? (
                  <Icons.loader className="h-4 w-4 animate-spin" />
                ) : (
                  <Icons.send className="h-4 w-4" />
                )}
              </Button>
            </div>
          </div>
        </div>
      ) : (
        <button
          onClick={() => setIsOpen(true)}
          className="bg-loomi-primary text-white p-4 rounded-full shadow-lg hover:bg-loomi-dark transition-colors"
        >
          <Icons.message className="h-6 w-6" />
        </button>
      )}
    </div>
  );
}
