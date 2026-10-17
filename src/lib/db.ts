import path from 'path';

let _dbInstance: any = null;

export function getDb() {
  if (_dbInstance) {
    return _dbInstance;
  }

  try {
    const fs = require('fs');
    let dbPath = path.resolve(process.cwd(), 'f4f_community.db');
    if (process.env.VERCEL || process.env.AWS_LAMBDA_FUNCTION_NAME) {
      const tmpPath = '/tmp/f4f_community.db';
      if (!fs.existsSync(tmpPath) && fs.existsSync(dbPath)) {
        try {
          fs.copyFileSync(dbPath, tmpPath);
        } catch (copyErr) {
          console.error('Failed to copy seed db to /tmp:', copyErr);
        }
      }
      if (fs.existsSync(tmpPath)) {
        dbPath = tmpPath;
      }
    }

    const { DatabaseSync } = require('node:sqlite');
    const db = new DatabaseSync(dbPath);

    // Apply high-performance SQLite PRAGMAs
    db.exec(`
      PRAGMA foreign_keys = ON;
      PRAGMA busy_timeout = 30000;
      PRAGMA synchronous = NORMAL;
      PRAGMA cache_size = -64000;
      PRAGMA temp_store = MEMORY;
      PRAGMA journal_mode = WAL;
    `);

    _dbInstance = db;
    return db;
  } catch (error) {
    console.error('Failed to initialize local SQLite database:', error);
    throw error;
  }
}

export function query<T = any>(sql: string, params: any[] = []): T[] {
  const db = getDb();
  const stmt = db.prepare(sql);
  return stmt.all(...params) as T[];
}

export function get<T = any>(sql: string, params: any[] = []): T | null {
  const db = getDb();
  const stmt = db.prepare(sql);
  const result = stmt.get(...params);
  return (result as T) || null;
}

export function run(sql: string, params: any[] = []): { changes: number; lastInsertRowid: number | bigint } {
  const db = getDb();
  const stmt = db.prepare(sql);
  return stmt.run(...params);
}

export function exec(sql: string): void {
  const db = getDb();
  db.exec(sql);
}

// Supabase Client Initialization (Optional / Dual-Mode)
let _supabaseClient: any = null;

export function getSupabase() {
  if (_supabaseClient) return _supabaseClient;
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY;

  if (url && key && !key.includes('placeholder')) {
    try {
      const { createClient } = require('@supabase/supabase-js');
      _supabaseClient = createClient(url, key);
      return _supabaseClient;
    } catch (e) {
      console.warn('Could not initialize Supabase client:', e);
    }
  }
  return null;
}
