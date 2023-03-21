import {
  Teste1,
  Teste2
} from 'index';

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
/**
 * Simple enum for testing 
 */
export enum SimpleEnum {
  one,
  two,
  /**
   * Testing 
   */
  three,
}
/**
 * Enum with defined numbers on options for testing 
 */
export enum EnumWithDefinedNumbersOnOptions {
  /**
   * One 
   */
  one = 1,
  two = 2,
  /**
   * Testing 
   */
  three = 3,
}
/**
 * Type with internal enum 
 */
export type TypeWithInternalEnum = {
  a: string;
  b: string;
  c: cEnum;
};

enum cEnum {
  /**
   * One 
   */
  one = 1,
  /**
   * Two 
   */
  two = 2,
}
