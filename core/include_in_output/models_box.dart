class ModelsBox<T, M> {
  final String _boxKey;
  final T Function(M data) _boxValueToValue;
  final M Function(T data) _valueToBoxValue;

  ModelsBox({
    required String boxKey,
    required T Function(M data) boxValueToValue,
    required M Function(T data) valueToBoxValue,
  })  : _boxKey = boxKey,
        _boxValueToValue = boxValueToValue,
        _valueToBoxValue = valueToBoxValue;

  late final Box<M> _box;

  Future<void> init() async {
    try {
      await Hive.openBox<M>(_boxKey);
    } on Exception {
      await Hive.deleteBoxFromDisk(_boxKey);
      await Hive.openBox<M>(_boxKey);
    }

    _box = Hive.box<M>(_boxKey);
  }

  Iterable<String> get keys => _box.keys;

  int get length => keys.length;

  bool get isEmpty => keys.isEmpty;

  bool get isNotEmpty => !isEmpty;

  T? get(String key) {
    final value = _box.get(key);
    if (value == null) return null;

    return _boxValueToValue(value);
  }

  Future<void> put(String key, T data) async {
    if (keys.contains(key)) {
      await delete(key);
    }
    await _box.put(key, _valueToBoxValue(data));
  }

  Future<void> delete(String key) => _box.delete(key);

  Iterable<T> get values => _box.values;

  Future<void> clear() => _box.clear();
}
