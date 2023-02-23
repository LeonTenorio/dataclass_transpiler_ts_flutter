import {
  Teste1,
  Teste2
} from 'index.dart';

/**
 * Basic type 
 */
export type BasicType = {
  /**
   * Basic type a object field comment 
   */
  a: string;
  b: string;
  c: string;
};

export type BasicTypeWithNullableAndOptional = {
  a: string | null;
  b?: string;
  c: string;
};

export type TypeWithUnion = {
  c: string;
  d: string;
} | BasicType;

export type TypeWithMultipleUnion = 
  | {
  c: string;
  d: string;
} | BasicType
  | BasicTypeWithNullableAndOptional;

export type TypeWithIntersection = {
  e: string;
} & BasicType;

export type TypeWithMultipleIntersection = 
  & {
  e: string;
} & BasicType
  & BasicTypeWithNullableAndOptional;

/**
 * Nested type 
 */
export type NestedType = {
  a: string;
  b: string;
  c: {
    a: string;
  };
};

